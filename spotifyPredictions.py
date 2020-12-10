import pandas as pd
import sklearn.model_selection as ms
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, plot_confusion_matrix, classification_report, accuracy_score
from sklearn import svm
import pickle
import seaborn as sea
import matplotlib.pyplot as plt



model = 'spotify_model_NN.sav'
testSongs = pd.read_csv("allSongs.csv")
X = testSongs[['Acousticness','Danceability','Energy','Instrumentalness','Liveness','Loudness','Speechiness','Valence','Tempo','Popularity']]

loaded_model = pickle.load(open(model, 'rb'))

y_pred = loaded_model.predict(X)
y_score = loaded_model.predict_proba(X)

testSongs['Predict'] = y_pred
testSongs['Karaokability'] = y_score[:,1]

testSongs = testSongs.sort_values(by=['Karaokability'],ascending=False)

testSongs.to_csv("songRanks_NN.csv",index=False)

plt.rcParams.update({'font.size': 3})

corr = testSongs.corr()
heat = sea.heatmap(corr)

plt.savefig("corrPOST_PREDICT_NN.png",transparent=True,dpi=275,pad_inches=0)
plt.clf()
