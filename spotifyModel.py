import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sea
import sklearn.model_selection as ms
import scipy as sp
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, plot_confusion_matrix, classification_report, accuracy_score
from sklearn import svm
from sklearn.neural_network import MLPClassifier
import pickle


good = pd.read_csv("song-features.csv")
bad = pd.read_csv("bad-song-features.csv")
good['Good'] = 1
bad['Good'] = 0

plt.rcParams.update({'font.size': 3})

allSongs = pd.concat([good,bad])
corr = allSongs.corr()
heat = sea.heatmap(corr)

plt.savefig("corrHeatMap.png",transparent=True,dpi=275,pad_inches=0)
plt.clf()
plt.rcParams.update({'font.size': 10})


highcorr = corr[abs(corr)>.4]
#Features with the highest corrilation to whether a song is good for Karaoke or not
#Acousticness,Instrumentalness,Loudness,Popularity


X = allSongs[['Acousticness','Danceability','Energy','Instrumentalness','Liveness','Loudness','Speechiness','Valence','Tempo','Popularity']]
Y = allSongs['Good']

#X_train, X_test, y_train, y_test = ms.train_test_split(X, Y, test_size=0.2, random_state=42)

#LOGIT
# log_reg = LogisticRegression()
# log_reg.fit(X,Y)
# filename = 'spotify_model_logit.sav'
# pickle.dump(log_reg, open(filename, 'wb'))

#SVM
#svm_model = svm.SVC(probability=True)
# svm_model.fit(X,Y)
# filename = 'spotify_model_svm.sav'
# pickle.dump(svm_model, open(filename, 'wb'))
#svm_model.fit(X_train,y_train )

#Neural neural_network
#NN =  MLPClassifier()
#NN.fit(X,Y)
#NN.fit(X_train,y_train )
# filename = 'spotify_model_NN.sav'
# pickle.dump(NN, open(filename, 'wb'))


# y_pred = log_reg.predict(X_test)
# y_pred = svm_model.predict(X_test)
#y_pred = NN.predict(X_test)

# confusion_matrix(y_test, y_pred)
#
# plot_confusion_matrix(NN, X_test, y_test) # (estimator, X, y_true)
# plt.savefig('confusion_matrixNNs.png',transparent=True,dpi=275,pad_inches=0)

#prints accuracy scorre and classsification report
# print("accuracy score:", accuracy_score(y_test, y_pred))
# print(classification_report(y_test, y_pred, labels=[0, 1, 2]))
