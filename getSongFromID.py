import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os


client_id = "1cc2b52f7c6447409439ddc56223fb26"
client_secret = "c1e05ecad59f4208aea0fb91d79fdbd4"
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

track = spotify.track("5bWqohZFWxcJK7zkReX8Jg")
url = track['preview_url']

if url is not None:
    command = "wget -O " + "song.mp3 \"" + url +"\""
    os.system(command)
