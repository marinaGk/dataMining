import pandas as pd 
import csv
import os

def return_day(year, month, day): 
    '''Returns part of dataframe regarding requested date'''

    real_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(real_path)
    os.chdir(dir_path)

    df_file_path = dir_path + "\\merged_source_files.csv"
    df = pd.read_csv(df_file_path)
    
    dateDf = df[df['Day'] == day]
    dateDf = dateDf[dateDf['Month'] == month]
    dateDf = dateDf[dateDf['Year'] == year] 
    dateDf.reset_index(inplace = True, drop=True)

    return dateDf

def return_year(year): 
    '''Returns part of dateframe regarding requested year'''

    real_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(real_path)
    os.chdir(dir_path)

    df_file_path = dir_path + "\\merged_source_files.csv"
    df = pd.read_csv(df_file_path)

    yearDf = df[df['Year'] == year]
    yearDf.reset_index(inplace = True, drop=True)

    return yearDf


