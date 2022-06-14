import vlc #importing vlc module
import serial #importing serial module            )
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
for i in range(2000):
	print("waiting")
player.pause()
