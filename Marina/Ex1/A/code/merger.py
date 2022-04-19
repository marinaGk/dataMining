import pandas as pd 
import csv
import os

def merge(): 
    '''Creates dataframe containing all info, returns it'''

    real_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(real_path)
    dir_path = dir_path[0:-4] + "sources\\"
    os.chdir(dir_path) #works inside data directory (sources)

    filelist = []
    row_count = 0 
    days = []
    months = []
    years = []

    df = pd.DataFrame() #dataFrame to be used to store data 

    for filename in os.listdir(dir_path):

        file = dir_path + filename

        if ((os.stat(file).st_size == 0) == False):

            row_count = len(pd.read_csv(file)) #counts amount of rows per day in order to add its date same amount of times to 'Date' column on database
            #didn't try to make subrows since, either way, key for each row is both date and time

            days = days + [filename[6:8]]*row_count
            months = months + [filename[4:6]]*row_count
            years = years + [filename[0:4]]*row_count

            filelist.append(file) 

    df = pd.concat(map(pd.read_csv, filelist), ignore_index=True) #reads and concatenates all resource files into one dataframe 
    df.insert(0, 'Day', days) #adds day column
    df.insert(1, 'Month', months) #adds month column 
    df.insert(2, 'Year', years) #adds year column

    return df

def return_day(df, year, month, day): 
    '''Returns part of dataframe regarding requested date'''

    dateDf = df[df['Day'] == day]
    dateDf = dateDf[dateDf['Month'] == month]
    dateDf = dateDf[dateDf['Year'] == year]

    return dateDf 

def return_year(df, year): 
    '''Returns part of dateframe regarding requested year'''

    yearDf = df[df['Year'] == year]

    return yearDf


