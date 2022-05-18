from datetime import datetime, timedelta
import pandas as pd
from day_data import make_day_dataframe
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, LSTM
from merger import *
import numpy as np

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

def additional(): 
    '''Makes additional columns in dataFrame to be used in LSTM model'''

    df = merge()
    
    df['Date'] = pd.to_datetime(df['Year'] + "-" + df['Month'] + "-" + df["Day"])
    df['Weekday'] = df['Date'].dt.dayofweek
    df['Energy_at_timestamp'] = ''
    df['Day_average'] = ''
    df['Weekday_average'] = ''

    weekday_avg = [0, 0, 0, 0, 0, 0, 0]
    counter = [0, 0, 0, 0, 0, 0, 0]

    date = df['Date'].iloc[0]
    lastDate = df['Date'].iloc[-1]

    while (date != lastDate + pd.to_timedelta(1, unit='d')):

        row = df.loc[df['Date'] == date]
        current_date = row.iloc[0]
        weekday = current_date['Weekday']

        dayDf = make_day_dataframe(df, current_date['Year'], current_date['Month'], current_date['Day'])

        avg = dayDf['Sums'].mean()

        weekday_avg[weekday] += avg
        counter[weekday] += 1

        df.loc[df['Date'] == date, 'Energy_at_timestamp'] = dayDf['Sums']

        df.loc[df['Date'] == date, 'Day_average'] = avg
        
        date = current_date['Date'] + pd.to_timedelta(1, unit='d')

    for i in range(7): 
        df.loc[df['Weekday'] == i, 'Weekday_average'] = weekday_avg[i]/counter[i]

    return df

def prediction(): 

    df = additional()
    predictors = df[['Weekday', 'Energy_at_timestamp', 'Weekday_average']]
    target = df[['Day_average']]

    scaler = MinMaxScaler(feature_range=(0,1))

    X = scaler.fit_transform(predictors)
    y = scaler.fit_transform(target)

    pred_train, pred_test, tar_train, tar_test = train_test_split(X, y, test_size=0.3, random_state=42)

    x_train = []
    y_train = []

    for i in range(288, len(pred_train)):
        x_train.append(pred_train[i-288:i, 0:3])
        y_train.append(tar_train[i, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], x_train.shape[2], 1))

    model = Sequential()

    model = Sequential()
    model.add(Dense(units=5, input_dim=3, kernel_initializer='normal', activation='relu'))
    model.add(Dense(units=5, kernel_initializer='normal', activation='tanh'))
    model.add(Dense(1, kernel_initializer='normal'))
    model.compile(loss='mean_squared_error', optimizer='adam')

    model.fit(x_train, y_train, batch_size=1, epochs=1)

    x_test = []
    y_test = target[-(len(tar_test)+1):, 0]

    for i in range(288, len(pred_test)): 
        x_test.append(pred_test[i-288:i, 0:3])

    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], x_test.shape[2], 1 ))


    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)
    print(predictions)

prediction()