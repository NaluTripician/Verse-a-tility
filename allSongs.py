import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import numpy as np
import pandas as pd
import time

username = 'nalutrip'
client_id = "1cc2b52f7c6447409439ddc56223fb26"
client_secret = "c1e05ecad59f4208aea0fb91d79fdbd4"
uri = "https://dknopf.github.io/Verse-a-tility"

scope = "playlist-read-private,user-read-private,playlist-read-collaborative,user-library-read"

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) #creates spotify object to access API

token = util.prompt_for_user_token(username,scope,client_id=client_id,client_secret=client_secret,redirect_uri=uri)

sp = spotipy.Spotify(auth=token)

userID = sp.me()['id']
playlists = sp.user_playlists(userID) #gives a Dictionary of user playlists
library1 = sp.current_user_saved_tracks(limit=50,offset=0)
library2 = sp.current_user_saved_tracks(limit=50,offset=50)
library3 = sp.current_user_saved_tracks(limit=50,offset=100)
library4 = sp.current_user_saved_tracks(limit=50,offset=150)
library5 = sp.current_user_saved_tracks(limit=50,offset=200)
library6 = sp.current_user_saved_tracks(limit=50,offset=250)
library7 = sp.current_user_saved_tracks(limit=50,offset=300)
library8 = sp.current_user_saved_tracks(limit=50,offset=350)
library9 = sp.current_user_saved_tracks(limit=50,offset=400)
library10 = sp.current_user_saved_tracks(limit=50,offset=450)

libs= [library1,library2,library3,library4,library5,library6,library7,library8,library9,library10]

alblums = sp.current_user_saved_albums(limit=50)

songs = {}


for library in libs:
    for song in library['items']:
            songs[song['track']['id']] = (song['track']['name'], song['track']['artists'][0]['name'], song['track']['popularity'])

print('lib')

for album in alblums['items']:
    for song in album['album']['tracks']['items']:
        songs[song['id']] = (song['name'],song['artists'][0]['name'],sp.track(song['id'])['popularity'])

print('alb')

for playlist in playlists['items']:
    """
    Each iteration of the loop gets all the songs for that playlist
    """
    songDict = sp.user_playlist(userID, playlist['id'], fields="tracks")
    playlistSongs = songDict['tracks']

    for i in range(len(playlistSongs['items'])):
        try:
            #id: (title,artist,popularity)
            songs[playlistSongs['items'][i]['track']['id']]=(playlistSongs['items'][i]['track']['name'],playlistSongs['items'][i]['track']['artists'][0]['name'],(playlistSongs['items'][i]['track']['popularity']))
        except:
            pass #for empty playlist
print('play')

"""
Dictionary (userSongs) Format:
songID: (songTitle,songArtist,(acousticness,danceability,energy,instrumentalness,liveness,loudness,speechiness,valence,tempo))
"""
songList = songs.items()
allSongs = {}
for song in songList:
    """
    Audio analysis for all user songs
    """
    songID = song[0]
    songTitle = song[1][0]
    songArtist = song[1][1]
    popularity = song[1][2]
    try:
        features = sp.audio_features(songID)[0]

        acousticness = features['acousticness']
        danceability = features['danceability']
        energy = features['energy']
        instrumentalness = features['instrumentalness']
        liveness = features['instrumentalness']
        loudness = (features['loudness'])
        speechiness = features['speechiness']
        valence = features['valence']
        tempo = features['tempo']
        allSongs[songID] = [songTitle,songID,acousticness,danceability,energy,instrumentalness,liveness,loudness,speechiness,valence,tempo,popularity]
    except:
        pass

trainNP = pd.read_csv("song-features.csv").to_numpy()
for song in trainNP:
    allSongs[song[1]] = song.tolist()
"""
<*><*><*><*><*><*><*><*><*><*><*><*><*><*><*><*>
"""

labels = ['Title','Artist','Acousticness','Danceability','Energy','Instrumentalness','Liveness','Loudness','Speechiness','Valence','Tempo','Popularity']
df = pd.DataFrame.from_dict(allSongs,orient='index',columns=labels)

df.to_csv('allSongs.csv',index=False)
