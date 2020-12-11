import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import os


ranks = pd.read_csv("songRanks_NN.csv").ID
best1 = ranks[:50]
best2 = ranks[50:100]
best3 = ranks[100:150]
best4 = ranks[150:200]
worst1 = ranks[-50:]
worst2 = ranks[-100:-50]
worst3 = ranks[-150:-100]
worst4 = ranks[-200:-150]

sets=[  [("Dataset/Good/",best1),("Dataset/Good/",best2),("Dataset/Good/",best3),("Dataset/Good/",best4)],
        [("Dataset/Bad/",worst1),("Dataset/Bad/",worst2),("Dataset/Bad/",worst3),("Dataset/Bad/",worst4)]]

client_id = ""
client_secret = ""

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

i = 0

for cat in sets:
    num = 0
    for loc, set in cat:
        results = spotify.tracks(set)
        for track in results['tracks']:
            if(track['preview_url'] is not None):
                command = "wget -O " + loc + str(num) + ".mp3 \"" + track['preview_url'] +"\""
                num+=1
                os.system(command)
