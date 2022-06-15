import os, glob, serial, eyed3
import random
import time
from serial import Serial
import vlc
import mutagen.mp3
from time import sleep
from pygame import mixer


def serialInit():
    #Configure the serial port
   # ser = serial.Serial(
     #       '/dev/ttyUSB0',  #port detected for Arduino board
    #        9600,  #baud rate for serial communication
   #         timeout=0,
  #          bytesize=serial.EIGHTBITS,
 #           parity=serial.PARITY_NONE,
#            stopbits=serial.STOPBITS_ONE)
    ser = serial.Serial("/dev/ttyUSB0", baudrate = 9600, parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0)
    return ser

#   https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
def contenidoMusical():
    """
        Esta funcion regresa una lista con los archivos .mp3
        del directorio.
        
    """
    #   Obtiene la lista de los archivos en la carpeta
    listaMusica = os.listdir()
    tempList = []
    #   Para cada elemento en la lista, borra los que no son .mp3
    for i in listaMusica:
        #   Si el elemento de la lista no termina con 3, lo borra.
        if(i[-1] != '3'or i[-1] == 'y'):
            continue
        else:
            tempList.append(i)
            #print(i[-2:-1])
    print(tempList)
    return tempList

#   Se definen las funciones de musica()
def playMusica(listaMusica):
    """
        Esta función inicializa el mixer de la librería pygame
        para cargar una canción y reproducirla.
    """
    #   Se inicializa el mixer.
    mp3 = mutagen.mp3.MP3(listaMusica[0])
    mixer.init(frequency=mp3.info.sample_rate)
    #   Se define volumen y carga canción.
    mixer.music.load(listaMusica[0])
    #   Le pone volumen mínimo a la canción.
    #   Limite de volumen es de 0 a 1.
    mixer.music.set_volume(0.9)
def initFreq(listaMusica, index):
    mp3 = mutagen.mp3.MP3(listaMusica[index])
    mixer.init(frequency=mp3.info.sample_rate)
#   Regresa una lista con datos de la canción.
def getSongStuff(listaMusica, index):
    """
        Esta función retorna datos metadata de la canción.
        El orden de los datos es el siguiente:
        0    Nombre del archivo
        1    Título de la canción
        2    Artista
        3    Álbum
        4    Año de publicación
        5    Género

        Regresa la lista con dichos datos.
    """
    #   Carga una instancia de la libreria que guarda los metadatos
    cancionStuff = eyed3.load(listaMusica[index])
    #   Lista que guarda los datos generales de la canción
    listaDatos = [listaMusica[index], cancionStuff.tag.title,
             cancionStuff.tag.artist, cancionStuff.tag.album,
             cancionStuff.tag.release_date, cancionStuff.tag.genre]
    return listaDatos

def checkIndex(listaMusica, index, tipo):
    """
        Esta función es para revisar los índices
        y evitar tronarla por error de indexación
        Regresa el valor del indice
    """
    #   Si el caracter es M, es para subir
    if(tipo == 'M'):
        #   Si el indice es mayor al tamaño de la lista
        if(index >= len(listaMusica)-1):
            #   Regresa a la cancion 0
            index = 0
        else:
            #   Incrementa el indice de la lista de canciones (baja en la lista)
            index += 1
     #   Si el caracter es M, es para bajar
    if(tipo == 'm'):
        #   Si el indice es menor a 0
        if(index <= 0):
            #   Incrementa el indice de la lista de canciones (baja en la lista)
            index = len(listaMusica)-1
        else:
            #   Decrementa el indice de la lista de canciones (sube en la lista)
            index -= 1 
    return index

def shuffle(listaMusica, index):
    """
        Esta función genera un indice aleatorio
        para seleccionar aleatoriamente una canción.
        Regresa un índice aleatorio.
    """
    rIndex = random.randint(0, (len(listaMusica)-1) )
    while(rIndex == index):
        rIndex = random.randint(0, (len(listaMusica)-1) )
    return rIndex



def reproducingMusic():
    """
        Esta funcion reproduce la musica
    """
    #  Genera una instancia de la lista de música adentro de la carpeta
    listaMusica = contenidoMusical()
    #   Inicializa la reproducción de la música
    playMusica(listaMusica)
    #   Objeto serial
    ser = serialInit()

    #   Inicia a sonar la música
    mixer.music.play()
    #   Volumen 
    volumen = 0.1
    #  Índice de inicialización
    index = 0
    #   0  es volumen temporal, 2 es contadorMute
    auxParam = [volumen, 0]
    metadatos = getSongStuff(listaMusica, index)
    while(1):
        #   a es el input que recibe del teclado matricial
        #teclado = input("Ingresa si quieres subir volumen o bajar: ")
        #   Lee un valor del teclado matricial
        teclado = ser.read().decode('ascii')
        print(teclado)
        #   Si el botón 2 es presionado, sube el volumen de la canción
        if(teclado == '6'):
            volumen += 0.1
        #   Si el botón 2 es presionado, baja el volumen de la canción
        elif(teclado == '4'):
            volumen -= 0.1
        #   Si el botón 2 es presionado, 
        elif(teclado == '2'):
            print(len(listaMusica))
            #   Actualiza el valor del indice para que suba en la lista
            index = checkIndex(listaMusica, index, 'm')
        #   Si el botón 8 es presionado, 
        elif(teclado == '8'):
            #   Actualiza el valor del indice para que baje en la lista
            index = checkIndex(listaMusica, index, 'M')
        #   Si el botón 5 es presionado, se selecciona una canción nueva
        elif(teclado == '5'):
            #   Carga la canción del indice actual
            mixer.music.load(listaMusica[index])
            #   Carga los datos de la canción del indice actual
            metadatos = getSongStuff(listaMusica, index)
            initFreq(listaMusica, index)
            #   Reproduce la canción
            mixer.music.play()
        #   Si el botón 1 es presionado, se reproduce la canción anterior
        elif(teclado == '1'):
            #   Regresa el indice dependiendo de si se acabó la lista o no
            index = checkIndex(listaMusica, index, 'm')
            try:
                #   Carga la canción del indice previo
                mixer.music.load(listaMusica[index])
                #   Carga los datos de la canción del indice actual
                metadatos = getSongStuff(listaMusica, index)
                #   Reproduce la canción
                initFreq(listaMusica, index)
                mixer.music.play()
            except:
                print("El indice o el archivo es invalido, o se acabó la lista de canciones")
                #   Carga la primer canción de la lista
                mixer.music.load(listaMusica[0])
                #   Carga los datos de la canción del indice actual
                metadatos = getSongStuff(listaMusica, 0)
                #   Reproduce la canción
                initFreq(listaMusica, index)
                mixer.music.play()
        #   Si el botón 3 es presionado, se reproduce la canción siguiente
        elif(teclado == '3'):
            #   Regresa el indice dependiendo de si se acabó la lista o no
            index = checkIndex(listaMusica, index, 'M')
            try:
                #   Carga la canción del siguiente indice
                mixer.music.load(listaMusica[index])
                #   Carga los datos de la canción del indice actual
                metadatos = getSongStuff(listaMusica, index)
                #   Reproduce la canción
                initFreq(listaMusica, index)
                mixer.music.play()
            except:
                print("El indice o el archivo es invalido, o se acabó la lista de canciones")
                #   Carga la última canción
                mixer.music.load(listaMusica[len(listaMusica)-1])
                #   Carga los datos de la canción del indice actual
                metadatos = getSongStuff(listaMusica, len(listaMusica)-1)
                #   Reproduce la canción
                initFreq(listaMusica, index)
                mixer.music.play()

        #   Si el botón 7 es presionado,
        elif(teclado == '7'):
            #   Pausa la canción
            mixer.music.pause()
        #   Si el botón 9 es presionado,
        elif(teclado == '9'):
            #   Reproduce la canción
            mixer.music.unpause()
        #   Si la tecla # es presionada, Mutea por completo el volumen
        elif(teclado == '#'):
            #   Si el contador de mute es 0, se pone en Mute
            if(auxParam[1] == 0):
                auxParam[0] = volumen
                volumen = 0
                auxParam[1] = 1
            #   De lo contrario, se reestablece el volumen previo al Mute
            elif(auxParam[1] == 1):
                auxParam[1] = 0
                volumen = auxParam[0]
        elif(teclado == '*'):
            #   Genera un indice aleatorio
            index = shuffle(listaMusica, index)
             #   Carga la canción del siguiente indice
            mixer.music.load(listaMusica[index])
            #   Carga los datos de la canción del indice actual
            metadatos = getSongStuff(listaMusica, index)
            #   Reproduce la canción
            initFreq(listaMusica, index)
            mixer.music.play()
        elif(teclado == '@'):
            #   Itera en cada elemento de los metadatos
            for i in metadatos:
                #   Manda el elemento actual de los metadatos en formato ascii
                #ser.write(str(i).encode('ascii') )
                print(str(i).encode('ascii') )
        #   Si presiona A, muere el programa
        elif(teclado == 'A'):
            break
        #   Ajusta el volumen con el nuevo valor
        mixer.music.set_volume(volumen)
        #   Muestra el archivo de la canción actual
        print(listaMusica[index])
    #   Para la reproducción de musica
    mixer.music.stop()

#   Ejecuta la funcion principal
reproducingMusic()
