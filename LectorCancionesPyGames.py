import os
import glob
import eyed3
from pygame import mixer


#   https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
def contenidoMusical():
    listaMusica = os.listdir()
    return listaMusica

#   Se definen las funciones de musica()
def playMusica(listaMusica):
    """
        Esta función inicializa el mixer de la librería pygame
        para cargar una canción y reproducirla.
    """
    #   Se inicializa el mixer.
    mixer.init()
    #   Se define volumen y carga canción.
    mixer.music.load(listaMusica[4])
    #   Le pone volumen mínimo a la canción.
    #   Limite de volumen es de 0 a 1.
    mixer.music.set_volume(0.1)

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

def reproducingMusic():
    """
        Esta funcion reproduce la musica
    """
    ##  Genera una instancia de la lista de música adentro de la carpeta
    listaMusica = contenidoMusical()
    #   Inicializa la reproducción de la música
    playMusica(listaMusica)

    
    #   Inicia a sonar la música
    mixer.music.play()
    volumen = 0.1
    temp = volumen
    contMute = 0
    index = 4

    while(1):
        #   a es el input que recibe del teclado matricial
        teclado = input("Ingresa si quieres subir volumen o bajar: ")
        #   Si el botón 2 es presionado, sube el volumen de la canción
        if(teclado == '6'):
            volumen += 0.1
        #   Si el botón 2 es presionado, baja el volumen de la canción
        elif(teclado == '4'):
            volumen -= 0.1
        #   Si el botón 2 es presionado, 
        elif(teclado == '2'):
            #   Decrementa el indice de la lista de canciones (sube en la lista)
            index -= 1
        #   Si el botón 8 es presionado, 
        elif(teclado == '8'):
            #   Incrementa el indice de la lista de canciones (baja en la lista)
            index += 1
        #   Si el botón 5 es presionado, se selecciona una canción nueva
        elif(teclado == '5'):
            #   Carga la canción del indice actual
            mixer.music.load(listaMusica[index])
            #   Carga los datos de la canción del indice actual
            metadatos = getSongStuff(listaMusica, index)
            #   Reproduce la canción
            mixer.music.play()
        #   Si el botón 1 es presionado, se reproduce la canción anterior
        elif(teclado == '1'):
            try:
                #   Carga la canción del indice previo
                mixer.music.load(listaMusica[index - 1])
                #   Carga los datos de la canción del indice actual
                metadatos = getSongStuff(listaMusica, index)
                #   Reproduce la canción
                mixer.music.play()
            except:
                print("El indice o el archivo es invalido, o se acabó la lista de canciones")
                #   Carga la primer canción de la lista
                mixer.music.load(listaMusica[0])
                #   Carga los datos de la canción del indice actual
                metadatos = getSongStuff(0)
                #   Reproduce la canción
                mixer.music.play()
        #   Si el botón 3 es presionado, se reproduce la canción siguiente
        elif(teclado == '3'):
            try:
                #   Carga la canción del siguiente indice
                mixer.music.load(listaMusica[index + 1])
                #   Carga los datos de la canción del indice actual
                metadatos = getSongStuff(listaMusica, index + 1)
                #   Reproduce la canción
                mixer.music.play()
            except:
                print("El indice o el archivo es invalido, o se acabó la lista de canciones")
                #   Carga la última canción
                mixer.music.load(listaMusica[len(listaMusica)-1])
                #   Carga los datos de la canción del indice actual
                metadatos = getSongStuff(listaMusica, len(listaMusica)-1)
                #   Reproduce la canción
                mixer.music.play()

        #   Si el botón 7 es presionado,
        elif(teclado == '7'):
            #   Pausa la canción
            mixer.music.pause()
        #   Si el botón 9 es presionado,
        elif(teclado == '9'):
            #   Reproduce la canción
            mixer.music.unpause()
        #   Si la tecla # es presoinada, Mutea por completo el volumen
        elif(teclado == '#'):
            #   Si el contador de mute es 0, se pone en Mute
            if(contMute == 0):
                temp = volumen
                volumen = 0
                contMute = 1
            #   De lo contrario, se reestablece el volumen previo al Mute
            elif(contMute == 1):
                contMute = 0
                volumen = temp
        elif(teclado == '0'):
            break

        mixer.music.set_volume(volumen)
    #   Para la reproducción de musica
    mixer.music.stop()

#   Ejecuta la funcion principal
reproducingMusic()
