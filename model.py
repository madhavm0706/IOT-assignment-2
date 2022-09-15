
#importing all required libraries

import pandas as pd
from sklearn import model_selection
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from tensorflow import keras
from keras import Sequential
from keras.layers import Dense, Activation
from keras.losses import MeanSquaredError
from keras import optimizers

import numpy as np


############################ Model Training ############################
#Importing the dataset
dataset = pd.read_csv("data.csv")
X = dataset.iloc[:, [0,1]].values
Y = dataset.iloc[:, 2].values

# Splitting the dataset into the Training set and Test set
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3, random_state=0)

#scaling data
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)


#build sequential model
model = Sequential()
model.add(Dense(units= 256, activation= 'relu',input_dim = 2))
model.add(Dense(units= 128, activation = 'relu'))
model.add(Dense(units= 1, activation= 'relu'))


#model compile and training
model.compile(loss = 'MeanSquaredError',
              optimizer=keras.optimizers.Adam(learning_rate=0.01),
              metrics='mae'
)

model.fit(X_train,Y_train,epochs=600,verbose=0)

#Prediction
class waterflow_prediction:
  


  def prediction(Humidity, Temp):
    test=np.array([Humidity,Temp])
    test.shape=(1,2)
    test = sc.transform(test)
    return model.predict(test)

wflow = waterflow_prediction

import joblib 
joblib.dump(wflow,"waterflowrate.pk1")