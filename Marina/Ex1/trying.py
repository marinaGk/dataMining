from datetime import datetime, timedelta
import os
import pandas as pd
from day_data import make_day_dataframe
from year_data import return_stats
from tensorflow import keras
from merger import *

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
    print(df)

prediction()