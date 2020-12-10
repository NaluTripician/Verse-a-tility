import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import umap

good = pd.read_csv("song-features.csv")
bad = pd.read_csv("bad-song-features.csv")
good['Good'] = 1
bad['Good'] = 0



allSongs = pd.concat([good,bad])

X = allSongs[['Acousticness','Danceability','Energy','Instrumentalness','Liveness','Loudness','Speechiness','Valence','Tempo','Popularity']].to_numpy()
labels = X['ID'].to_numpy(dtype='int64')

# X = pd.read_csv("data.csv").drop(['filename'],axis=1)
# labels = X['label'].replace("Good",1).replace("Bad",0).to_numpy(dtype='int64')
# X = X.drop(['label'],axis=1)

colors = np.array(['#FF0000','#0000FF'])

reducer = umap.UMAP(n_neighbors=200,min_dist=.05,metric='mahalanobis')
embedding = reducer.fit_transform(X)

plt.rcParams.update({'font.size': 15})
plt.rcParams['axes.facecolor'] = 'black'
plt.clf()
plt.figure(figsize=(10,10))
plt.scatter(embedding[:,0], embedding[:,1], color=colors[labels], alpha=1, marker='.',s=10)
plt.ylabel('UMAP axis 2')
plt.xlabel('UMAP axis 1')
plt.savefig('UMAP-EXTRACT.pdf')
plt.clf()
