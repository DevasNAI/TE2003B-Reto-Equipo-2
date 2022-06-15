import os, glob, serial, eyed3
import random
import time
from serial import Serial
import vlc
import mutagen.mp3
from time import sleep
from pygame import mixer
import pygame,sys
from pygame.locals import*
import pygame_widgets
from pygame_widgets.button import Button



def upVolumen():
    global volumen
    volumen += 0.1
def downVolumen():
    global volumen
    volumen -= 0.1
    
def serialInit():
    #Configure the serial port
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
#   Lista de musica
listaMusica = contenidoMusical()
#   Volumen 
volumen = 0.5
#  Índice de inicialización
index = 4
#   0  es volumen temporal, 2 es contadorMute
auxParam = [volumen, 0]
def setVolumen():
    global volumen
    mixer.music.set_volume(volumen)

#   Se definen las funciones de musica()
def playMusica():
    """
        Esta función inicializa el mixer de la librería pygame
        para cargar una canción y reproducirla.
    """
    global listaMusica
    global index
    #   Se inicializa el mixer.
    mp3 = mutagen.mp3.MP3(listaMusica[index])
    mixer.init(frequency=mp3.info.sample_rate)
    #   Se define volumen y carga canción.
    mixer.music.load(listaMusica[index])
    #   Le pone volumen mínimo a la canción.
    #   Limite de volumen es de 0 a 1.
    mixer.music.set_volume(0.9)

#   Inicializa la frecuencia
def initFreq():
    global listaMusica, index
    mp3 = mutagen.mp3.MP3(listaMusica[index])
    mixer.init(frequency=mp3.info.sample_rate)
#   Regresa una lista con datos de la canción.

def getSongStuff():
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
    global listaMusica, index
    #   Carga una instancia de la libreria que guarda los metadatos
    cancionStuff = eyed3.load(listaMusica[index])
    #   Lista que guarda los datos generales de la canción
    listaDatos = [listaMusica[index], cancionStuff.tag.title,
             cancionStuff.tag.artist, cancionStuff.tag.album,
             cancionStuff.tag.release_date, cancionStuff.tag.genre]
    return listaDatos

metadatos = getSongStuff()

def checkIndex(tipo):
    """
        Esta función es para revisar los índices
        y evitar tronarla por error de indexación
        Regresa el valor del indice
    """
    global listaMusica, index
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

def shuffle():
    """
        Esta función genera un indice aleatorio
        para seleccionar aleatoriamente una canción.
        Regresa un índice aleatorio.
    """
    global listaMusica, index
    rIndex = random.randint(0, (len(listaMusica)-1) )
    while(rIndex == index):
        rIndex = random.randint(0, (len(listaMusica)-1) )
    return rIndex


def newMusic():
    global listaMusica, index
    #   Carga la canción del indice previo
    mixer.music.load(listaMusica[index])
    #   Carga los datos de la canción del indice actual
    metadatos = getSongStuff()
    #   Reproduce la canción
    initFreq()
    mixer.music.play()

def muteVolumen():
    global volumen, auxParam
    #   Si el contador de mute es 0, se pone en Mute
    if(auxParam[1] == 0):
        auxParam[0] = volumen
        volumen = 0
        auxParam[1] = 1
    #   De lo contrario, se reestablece el volumen previo al Mute
    elif(auxParam[1] == 1):
        auxParam[1] = 0
        volumen = auxParam[0]

def playPrevSong():
    global listaMusica, index
    #   Regresa el indice dependiendo de si se acabó la lista o no
    index = checkIndex('m')
def playNextSong():
    global listaMusica, index
    index = checkIndex('M')

#   Pausa
def pauseSong():
    mixer.music.pause()

def unpauseSong():
     #   Reproduce la canción
    mixer.music.unpause()

def stopPlaySong():
    #   Mata la canción
    mixer.music.stop()

def sendMetadatos():
     #   Itera en cada elemento de los metadatos
    for i in metadatos:
        for j in len(i):
            ser.write(str(i).encode('ascii') )




#   Inicializa la reproducción de la música
playMusica()
#   Objeto serial
#ser = serialInit()
#   Inicia a sonar la música
mixer.music.play()


# Set up Pygame
pygame.init()
root = pygame.display.set_mode((850, 600))
pygame.display.set_caption("Reto")

background = pygame.image.load("sinfonia.jpg").convert()

miFuente = pygame.font.Font(None,50)
miTexto = miFuente.render("Reproductor MP3", 0, (200, 60, 80))

miFuente2 = pygame.font.Font(None,40)
miTexto2 = miFuente2.render(metadatos[1], 0, (0, 0, 0))



# Creates the button with optional parameters
button1 = Button(
    # Mandatory Parameters
    root,  # Surface to place button on
    50,  # X-coordinate of top left corner
    100,  # Y-coordinate of top left corner
    300,  # Width
    150,  # Height

    # Optional Parameters
    text='Play',  # Text to display
    fontSize=50,  # Size of font
    margin=20,  # Minimum distance between text/image and edge of button
    inactiveColour=(200, 50, 0),  # Colour of button when not being interacted with
    hoverColour=(150, 0, 0),  # Colour of button when being hovered over
    pressedColour=(0, 200, 20),  # Colour of button when being clicked
    radius=20,  # Radius of border corners (leave empty for not curved)
    onClick=lambda: unpauseSong()  # Function to call when clicked on
)


button2= Button(
    # Mandatory Parameters
    root,  # Surface to place button on
    50,  # X-coordinate of top left corner
    300,  # Y-coordinate of top left corner
    300,  # Width
    150,  # Height

    # Optional Parameters
    text='Pause',  # Text to display
    fontSize=50,  # Size of font
    margin=20,  # Minimum distance between text/image and edge of button
    inactiveColour=(200, 50, 0),  # Colour of button when not being interacted with
    hoverColour=(150, 0, 0),  # Colour of button when being hovered over
    pressedColour=(0, 200, 20),  # Colour of button when being clicked
    radius=20,  # Radius of border corners (leave empty for not curved)
    onClick=lambda: pauseSong()  # Function to call when clicked on
)


button3 = Button(
    # Mandatory Parameters
    root,  # Surface to place button on
    500,  # X-coordinate of top left corner
    100,  # Y-coordinate of top left corner
    300,  # Width
    150,  # Height

    # Optional Parameters
    text='+',  # Text to display
    fontSize=50,  # Size of font
    margin=20,  # Minimum distance between text/image and edge of button
    inactiveColour=(200, 50, 0),  # Colour of button when not being interacted with
    hoverColour=(150, 0, 0),  # Colour of button when being hovered over
    pressedColour=(0, 200, 20),  # Colour of button when being clicked
    radius=20,  # Radius of border corners (leave empty for not curved)
    onClick=lambda: upVolumen()  # Function to call when clicked on
)


button4 = Button(
    # Mandatory Parameters
    root,  # Surface to place button on
    500,  # X-coordinate of top left corner
    300,  # Y-coordinate of top left corner
    300,  # Width
    150,  # Height

    # Optional Parameters
    text='-',  # Text to display
    fontSize=50,  # Size of font
    margin=20,  # Minimum distance between text/image and edge of button
    inactiveColour=(200, 50, 0),  # Colour of button when not being interacted with
    hoverColour=(150, 0, 0),  # Colour of button when being hovered over
    pressedColour=(0, 200, 20),  # Colour of button when being clicked
    radius=20,  # Radius of border corners (leave empty for not curved)
    onClick=lambda: downVolumen() # Function to call when clicked on
)


#tecladU = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '#', '*']
#   Se declara un objeto Serial
ser = serialInit()

while(1):
    #ru = random.randint(0, (len(tecladU)-1) )
    #   
    teclado = ser.read().decode('ascii')
    #   a es el input que recibe del teclado matricial
    #teclado = tecladU[8]
    #teclado = input("Ingresa si quieres subir volumen o bajar: ")
    #   Reproduce la canción anterior
    if(teclado == '1'):
        playPrevSong()
        newMusic()
    #   Sube en la lista de canciones
    elif(teclado == '2'):
        print(len(listaMusica))
        #   Actualiza el valor del indice para que suba en la lista
        playPrevSong()
    #   Sube en la lista de canciones
    elif(teclado == '3'):
            #   Regresa el indice dependiendo de si se acabó la lista o no
        playNextSong()
        newMusic()
    #   Si el botón 2 es presionado, baja el volumen de la canción
    elif(teclado == '4'):
        volumen -= 0.1
    #   Si el botón 5 es presionado, se reproduce la canción del índice
    elif(teclado == '5'):
        newMusic()
    #   Si el botón 6 es presionado, sube el volumen de la canción
    elif(teclado == '6'):
        volumen += 0.1
    #   Pausa la canción
    elif(teclado == '7'):
        pauseSong()
    #   Baja en la lista de canciones
    elif(teclado == '8'):
        playNextSong()
    #   Remueve el pausa
    elif(teclado == '9'):
        unpauseSong()
    #   Pone en mute la canción
    elif(teclado == '#'):
        muteVolumen()
    #   Reproduce una canción aleatoria
    elif(teclado == '*'):
        #   Genera un indice aleatorio
        shuffle()
        #   Reproduce la canción
        newMusic()
    elif(teclado == 'A'):
        break
    else:
        sendMetadatos()
    
    setVolumen()


    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()

    root.blit(background, [0,0])
    pygame_widgets.update(events)  # Call once every loop to allow widgets to render and listen

    root.blit(miTexto,(280, 20))
    root.blit(miTexto2,(350, 260))
    pygame.display.update()
#   Para la reproducción de musica
stopPlaySong()

#reproducingMusic()