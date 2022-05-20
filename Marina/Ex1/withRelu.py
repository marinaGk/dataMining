import pandas as pd
import numpy as np
import math

from tensorflow import keras 
from keras.models import Sequential
from keras.layers import * 
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.losses import MeanSquaredError
from keras.metrics import RootMeanSquaredError
from keras.optimizers import Adam
from keras.models import load_model
from dfPart import *


'''def edit_source_db(): 

    real_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(real_path)
    os.chdir(dir_path)

    df_file_path = dir_path + "\\merged_source_files.csv"
    df = pd.read_csv(df_file_path)

    del df['Coal']
    del df['Natural gas']
    del df['Nuclear']
    del df['Imports']
    del df['Other']

    df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])

    #df['Weekday'] = df['Date'].dt.dayofweek

    df['Energy_at_timestamp'] = ''
    df['Day_average'] = ''

    #df['Weekday_average'] = ''

    #weekday_avg = [0, 0, 0, 0, 0, 0, 0]
    #counter = [0, 0, 0, 0, 0, 0, 0]

    date = df['Date'].iloc[0]
    secondDate = date + pd.to_timedelta(1, unit = "d")
    lastDate = df['Date'].iloc[-1]
    cols = ['Solar','Wind','Geothermal','Biomass','Biogas','Small hydro','Large hydro','Batteries']

    while (date != lastDate + pd.to_timedelta(1, unit='d')):

        year = pd.to_datetime(date).year
        month = pd.to_datetime(date).month
        day = pd.to_datetime(date).day
        #row = df.loc[df['Date'] == date]
        #current_date = row.iloc[0]
        #weekday = current_date['Weekday']

        dayDf = make_day_dataframe(cols, year, month, day)
        avg = dayDf['Sums'].mean()

        #weekday_avg[weekday] += avg
        #counter[weekday] += 1

        df.loc[df['Date'] == date, ['Energy_at_timestamp', 'Day_average']] = [dayDf['Sums'], avg]
        #df.loc[df['Date'] == date, 'Day_average'] = avg
        date = date + pd.to_timedelta(1, unit='d')


        for i in range(7): 
            df.loc[df['Weekday'] == i, 'Weekday_average'] = weekday_avg[i]/counter[i]
    print("done")
    return df'''

'''def add_demands():

    sourcesDf = edit_source_db()
    sourcesDf.info()'''

def form_data(df, window_size): 

    npdf = df.to_numpy()
    X=[]
    y=[]

    for i in range(len(npdf)-window_size): 
        row = [[x] for x in npdf[i:i+window_size]]
        X.append(row)
        value = npdf[i+window_size]
        y.append(value)

    return np.array(X), np.array(y)

def make_model(X_train, y_train, X_val, y_val): 

    model = Sequential()
    model.add(InputLayer((5, 1)))
    model.add(LSTM(64))
    model.add(Dense(8, 'relu'))
    model.add(Dense(1, 'linear'))

    model.summary()

    cp = ModelCheckpoint('model/', save_best_only=True)
    es = EarlyStopping(monitor = 'val_loss', patience = 20, verbose = 1)

    model.compile(loss = MeanSquaredError(), optimizer=Adam(learning_rate=0.0001), metrics = [RootMeanSquaredError()])
    model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs = 100, callbacks = [es, cp])

def check_prediction(X_train, y_train, X_val, y_val, X_test, y_test): 

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
    
def make_prediction(): 

    real_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(real_path)
    os.chdir(dir_path)

    df_file_path = dir_path + "\\merged_files.csv"
    df = pd.read_csv(df_file_path)

    forPredDf = pd.DataFrame()
    forPredDf = df[['Sums','Renewable sums', 'Current demand']]

    difs = []
    for i, row in forPredDf.iterrows(): 
            difs.append(row['Current demand'] - row['Renewable sums'])
    forPredDf.insert(3, 'Difference', difs)
    forPredDf.info()

    df = pd.DataFrame()
    df = forPredDf['Difference']

    X, y = form_data(df, 5)

    train_len = math.ceil(len(df) * 0.8)
    val_len = math.ceil((len(df)-train_len) * 0.5)

    X_train, y_train = X[:train_len], y[:train_len]
    X_val, y_val = X[train_len:val_len+train_len], y[train_len:val_len+train_len]
    X_test, y_test = X[val_len+train_len:], y[val_len+train_len:]

    #make_model(X_train, y_train, X_val, y_val)
    check_prediction(X_train, y_train, X_val, y_val, X_test, y_test)

make_prediction()
