from sklearn import svm
from sklearn.neural_network import MLPClassifier
import pandas as pd
import numpy as np
import pickle


X = pd.read_csv("data.csv").drop(['filename'],axis=1)
Y = X['label'].replace("Good",1).replace("Bad",0).to_numpy(dtype='int64')
X = X.drop(['label'],axis=1)

NN =  MLPClassifier()
NN.fit(X,Y)
filename = 'NN2_Model.sav'
pickle.dump(NN, open(filename, 'wb'))
