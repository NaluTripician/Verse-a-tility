import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import csv
import pandas as pd

"""
Song Features we care about: acousticness,danceability,energy,instrumentalness,liveness,loudness,speechiness,valence,tempo

Generates a CSV with the song features for every karaoke song given by a CSV
Also generates an average feature set to be passed to a naive classifier

Need to make the first part a function, and then pass a variable for writing CSVs so that it can be imported without constantly writing the CSVs
"""

def setGenerator(write,filepath):
    # Spotify Authorization informnation
    client_id = "1cc2b52f7c6447409439ddc56223fb26"
    client_secret = "c1e05ecad59f4208aea0fb91d79fdbd4"

    token = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret, proxies=None).get_access_token()

    # Open CSV of song names
    fh = open(filepath, 'r')
    reader = csv.reader(fh, delimiter = ',')
    songs = []
    for line in reader:
        song = line
        songs.append(song)
    fh.close()

     # Access Spotify iteration
    spotify = spotipy.Spotify(token)

    ids = {}
    for song in songs:
        try:
            track = spotify.search(song, limit = 1, market = 'US')
            id = track['tracks']['items'][0]['id']
            name = track['tracks']['items'][0]['name']
            popularity = track['tracks']['items'][0]['popularity']
            ids[id] = (id,name,popularity)
        except:
            pass

    featureFrame = pd.DataFrame(columns=["Title", "ID", "Acousticness", "Danceability", "Energy", "Instrumentalness", "Liveness", "Loudness", "Speechiness", "Valence", "Tempo", "Popularity"])
    # Generating song features for each song given
    features = []
    n=1
    for id,name,popularity in ids.values():
        fts = spotify.audio_features(id)[0]
        try:
            flist = [name,id,fts['acousticness'],fts['danceability'],fts['energy'],fts['instrumentalness'],fts['liveness'],fts['loudness'],fts['speechiness'],fts['valence'],fts['tempo'],popularity]
            features.append(flist)
        except:
            pass
        if write:
            featureFrame.loc[n] = flist
            n+=1
    if write:
        featureFrame.to_csv("bad-song-features.csv",index=False)


    # Averaging all of the features together
    length = len(features)
    avg = [0,0,0,0,0,0,0,0,0,0]
    for list in features:
        for i in range(len(avg)):
            avg[i] += list[i+2]
    for i in range(len(avg)):
        avg[i] = avg[i]/length

    average = avg
    return average


res =setGenerator(True,"badSongs.csv")
results = ""
for i in res:
    results = results + (str(i) + ",")

open("avg.txt",'w').write(results)
