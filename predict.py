import librosa
import pandas as pd
import numpy as np
import os
import pathlib
import csv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pickle

#insert spotify developer credentials here

client_id = ""
client_secret = ""

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

pribt("Enter a song:")
query = input()

ID = spotify.search(query, limit = 1, market = 'US')['tracks']['items'][0]['id']
track = spotify.track(ID)
url = track['preview_url']

if url is not None:

    command = "wget -O " + "predict" + ".mp3 \"" + url +"\""
    os.system(command)

    command = "ffmpeg -i \'predict.mp3\' \'predict.wav\'"
    os.system(command)

    model1 = 'NN2_Model.sav'
    model2 = 'spotify_model_NN.sav'
    nn = pickle.load(open(model1, 'rb'))
    verse2 = pickle.load(open(model2, 'rb'))

    y, sr = librosa.load('predict.wav', mono=True)

    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    rmse = librosa.feature.rms(y=y)
    spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(y)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    data = [np.mean(chroma_stft), np.mean(rmse),np.mean(spec_cent),np.mean(spec_bw),np.mean(rolloff),np.mean(zcr)]
    for e in mfcc:
        data.append(np.mean(e))
    nnData = np.array([np.array(data)])

    nnPredict = nn.predict(nnData)
    nnProb = nn.predict_proba(nnData)

    features = spotify.audio_features(track['id'])[0]

    acousticness = features['acousticness']
    danceability = features['danceability']
    energy = features['energy']
    instrumentalness = features['instrumentalness']
    liveness = features['instrumentalness']
    loudness = (features['loudness'])
    speechiness = features['speechiness']
    valence = features['valence']
    tempo = features['tempo']

    verse2Data = np.array([acousticness,danceability,energy,instrumentalness,liveness,loudness,speechiness,valence,tempo,track['popularity']])
    verse2Data = verse2Data.reshape(1, -1)

    verse2Predict = verse2.predict(verse2Data)
    verse2Prob = verse2.predict_proba(verse2Data)

    print("\n\n\nRESULTS\n----------\n")
    print("Neural Net:\t",nnPredict[0],nnProb[0][nnPredict[0]])
    print("Spotify Model:\t", verse2Predict[0], verse2Prob[0][verse2Predict[0]])

    nBase = 1
    sBase = 1
    if(nnPredict[0] == 0):nBase *= -1
    if(verse2Predict[0] == 0): sBase *= -1

    nBase *= nnProb[0][nnPredict[0]]
    sBase *= verse2Prob[0][verse2Predict[0]]

    compPredict = 0
    if(nBase + sBase) > 0: compPredict = 1
    compScore = abs(nBase + sBase)/2
    print("Composite Score:", compPredict, compScore)
else:
    print("No download available")
