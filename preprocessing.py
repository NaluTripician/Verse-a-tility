# feature extractoring and preprocessing data
import librosa
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image
import pathlib
import csv

cmap = plt.get_cmap('inferno')

plt.figure(figsize=(10,10))
labels = 'Good Bad'.split()

header = 'filename chroma_stft rmse spectral_centroid spectral_bandwidth rolloff zero_crossing_rate'
for i in range(1, 21):
    header += f' mfcc{i}'
header += ' label'
header = header.split()

file = open('data.csv', 'w', newline='')
with file:
    writer = csv.writer(file)
    writer.writerow(header)


for l in labels:
    pathlib.Path(f'img_data/{l}').mkdir(parents=True, exist_ok=True)
    for sub,dir,files in os.walk("Dataset/" + l + "/"):
        for filename in files:
            if(filename.endswith(".wav")):
                songname = f'./' + sub + filename
                print(songname)
                y, sr = librosa.load(songname, mono=True)
                plt.specgram(y, NFFT=2048, Fs=2, Fc=0, noverlap=128, cmap=cmap, sides='default', mode='default', scale='dB');
                plt.axis('off');
                plt.savefig(f'img_data/{l}/{filename[:-3].replace(".", "")}.png')
                plt.clf()

                chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
                rmse = librosa.feature.rms(y=y)
                spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
                spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
                rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
                zcr = librosa.feature.zero_crossing_rate(y)
                mfcc = librosa.feature.mfcc(y=y, sr=sr)
                to_append = f'{filename} {np.mean(chroma_stft)} {np.mean(rmse)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}'
                for e in mfcc:
                    to_append += f' {np.mean(e)}'
                to_append += f' {l}'
                file = open('data.csv', 'a', newline='')
                with file:
                    writer = csv.writer(file)
                    writer.writerow(to_append.split())
