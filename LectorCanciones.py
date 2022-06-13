import vlc #importing vlc module
import serial #importing serial module
#Configure the serial port
ser = serial.Serial(
            '/dev/ttyACM0',  #port detected for Arduino board
            9600,  #baud rate for serial communication
            timeout=0,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE
            )

#create the instance for the vlc media player
instance = vlc.Instance('--aout=alsa')
#creating a new media player 
player = instance.media_player_new() 
#Creating a new  media object
#specify the file you want to open
media = instance.media_new("/home/RayoMcqueen37/Music/TE2003B-Reto-Equipo-2/pokemon-blackwhite-music-route-10.mp3") 
                                                             
#setting media object to the audio player
player.set_media(media) 
#play the audio in the audio player
player.play()
while True:
    #Wait until there is data waiting in the serial buffer
    if (ser.in_waiting > 0):
    #read the 8-bit data and decode to ascii
    line = ser.read().decode("Ascii")
    print(line)
    if line == 'a': 
        player.pause()
    else:
        pass
