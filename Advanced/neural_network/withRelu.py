''' 
Creates neural network to make energy requirement predictions. 

Works with dataframe containing differences of current demand and renewable energy production. 
Model contains LSTM layer and some hidden layers. It works with windows of five samples predicting a future, sixth one. 
According to data those translate to samples per five minutes. 
Calculations are applied recursively, for 100 epochs or less, depepnding on whether error increases or reduces with use of 
EarlyStopping checkpoint. 
Model saved is the one with less error by using ModelCheckpoint. 

For error calculation uses RMSE and MAE. 

Can be imported as module.

Requires `pandas` and `numpy` libraries for data manipulation, 
`math` library for calculations, 
`os` library for path manipulation, 
`keras` library to make model and prediction and 
`sklearn` library for error calculation.
'''

import pandas as pd
import numpy as np
import math
import os

from tensorflow import keras 
from keras.models import Sequential
from keras.layers import * 
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.losses import MeanSquaredError
from keras.metrics import RootMeanSquaredError
from keras.optimizers import Adam
from keras.models import load_model

import sklearn.metrics as metrics

def form_data(df, window_size): 
    '''
    Forms data to be used in model
    
    Parameters
    ---------- 
    df: pandas DataFrame 
        DataFrame containing non-renewable energy requirements
    window_size: integer 
        Size of window used to separate data 

    Returns
    -------
    X, y: nympy arrays
        Numpy arrays containing formed data
        For each element of X, containing window_size elements, there's an element of y
    '''

    npdf = df.to_numpy()
    X=[]
    y=[]

    for i in range(len(npdf)-window_size): #adds window size each time so it can't work till end of dataframe 

        row = [[x] for x in npdf[i:i+window_size]] #gets next 5 samples of data 
        X.append(row) 
        value = npdf[i+window_size] #gets actual value of sample to be predicted
        y.append(value)

    return np.array(X), np.array(y)

def make_model(X_train, y_train, X_val, y_val): 
    '''
    Makes the model
    
    Parameters
    ----------
    X_train: numpy array
        Numpy array containing training data 
        Each of its rows contains 5 values used to make prediction of non-renewable energy required as a 6th sample 
    y_train: numpy arrray
        Numpy array containing the actual value of non-renewable energy required -> actual value of 6th sample for each row of X_train
    X_val: numpy array 
        Numpy array containing evaluation data used to measure model accuracy 
        Each of its rows contains 5 values used to make prediction of non-renewable energy required as a 6th sample 
    y_val: numpy array 
        Numpy array containing actual value of non-renewable energy required -> actual value of 6th sample for each row of X_val
    '''

    model = Sequential()
    model.add(InputLayer((5, 1))) #input layer
    model.add(LSTM(64)) #lstm hidden layer
    model.add(Dense(8, 'relu')) #hidden layer
    model.add(Dense(1, 'linear')) #output 

    model.summary()

    cp = ModelCheckpoint('model/', save_best_only=True) #makes model on folder model saving only prediction with less error 
    es = EarlyStopping(monitor = 'val_loss', patience = 20, verbose = 1) #uses checkpoint that stops once error starts increasing instead of decreasing after waiting for 20 epochs

    model.compile(loss = MeanSquaredError(), optimizer=Adam(learning_rate=0.0001), metrics = [RootMeanSquaredError()]) #minimizes mean squared error using adam optimization
    model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs = 100, callbacks = [es, cp]) #runs for 100 epochs or less if error stops dropping 

def check_prediction(X_train, y_train, X_val, y_val, X_test, y_test): 
    '''
    Loads already made model and checks its predictions by printing 
    its results, the actual results and some error measurements using RMSE and MAE

    Parameters
    ----------
    X_train: numpy array 
        Numpy array containing training data 
        Each of its rows contains 5 values used to make prediction of non-renewable energy required as a 6th sample 
    y_train: numpy array
        Numpy array containing the actual value of non-renewable energy required -> actual value of 6th sample for each row of X_train
    X_val: numpy array
        Numpy array containing evaluation data used to measure model accuracy 
        Each of its rows contains 5 values used to make prediction of non-renewable energy required as a 6th sample 
    y_val: numpy array 
        Numpy array containing actual value of non-renewable energy required -> actual value of 6th sample for each row of X_val
    X_test: numpy array 
        Numpy array containing test data 
        Is of same shape as X_train with smaller length and is used to calculate final model accuracy
    y_test: numpy array
        Numpy array containing actual value of non-renewable energy required -> actual value of 6th sample for each row of X_test
    '''

    model1 = load_model('model/')

    train_predictions = model1.predict(X_train).flatten()
    train_results = pd.DataFrame(data = {"Train Predictions":train_predictions, 'Actuals':y_train})
    print(train_results)

    val_predictions = model1.predict(X_val).flatten()
    val_results = pd.DataFrame(data = {"Val Predictions":val_predictions, 'Actuals':y_val})
    print(val_results)

    test_predictions = model1.predict(X_test).flatten()
    test_results = pd.DataFrame(data = {"Test Predictions":test_predictions, 'Actuals':y_test})
    print(test_results)

    rmse = metrics.mean_squared_error(test_predictions, y_test)
    rmse = math.sqrt(rmse)
    print("Root mean squared error: ", rmse)

    mae = metrics.mean_absolute_error(test_predictions, y_test)
    print("Mean absolute error: ", mae)
    
def make_prediction(): 
    '''
    Uses merged data to find already known non renewable energy requirements and predict future ones
    '''

    real_path = os.path.realpath(__file__) #file path
    dir_path = os.path.dirname(real_path) #neural network
    root_path = os.path.dirname(dir_path) #root 

    current_path = "{}/data".format(root_path)
    os.chdir(current_path) #works inside data directory 

    #uses merged file to make calculations quicker
    df_file_path = current_path + "\\merged_files.csv"
    df = pd.read_csv(df_file_path)

    #keeps only necessary part of dataframe to work with 
    forPredDf = pd.DataFrame()
    forPredDf = df[['Sums','Renewable sums', 'Current demand']]

    #difference of current demand per five minutes and sum of renewable energy per five minutes is amoung of non renewable energy required
    difs = []
    for i, row in forPredDf.iterrows(): 
            difs.append(row['Current demand'] - row['Renewable sums'])
    forPredDf.insert(3, 'Difference', difs)
    forPredDf.info()

    df = pd.DataFrame()
    df = forPredDf['Difference']

    #forms data setting window size of 5 samples
    X, y = form_data(df, 5)

    #sets train, validation (and test) length and makes respective arrays
    train_len = math.ceil(len(df) * 0.8)
    val_len = math.ceil((len(df)-train_len) * 0.5)

    X_train, y_train = X[:train_len], y[:train_len]
    X_val, y_val = X[train_len:val_len+train_len], y[train_len:val_len+train_len]
    X_test, y_test = X[val_len+train_len:], y[val_len+train_len:]

    print(dir_path)
    os.chdir(dir_path)

    make_model(X_train, y_train, X_val, y_val)

    check_prediction(X_train, y_train, X_val, y_val, X_test, y_test)
