import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os


client_id = ""
client_secret = ""
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

track = spotify.track("5bWqohZFWxcJK7zkReX8Jg")
url = track['preview_url']

if url is not None:
    command = "wget -O " + "song.mp3 \"" + url +"\""
    os.system(command)
