import pandas as pd 
import os
from data_analysis.path import *

def return_day(year, month, day): 
    '''
    Returns part of dataframe regarding requested date
    
    Parameters
    ---------- 
    year: string 
        Year - of date whose graph is required - as string 
    month: string 
        Number of month - of date whose graph is required - as string 
    day: string 
        Number of day - of date whose graph is required - as strings
    
    Returns
    -------
    pandas DataFrame
        Part of DataFrame containing data regarding consumption on input date
    '''

    real_path = os.path.realpath(__file__) #file path
    real_path = resolve_path(real_path)
    dir_path = os.path.dirname(real_path) #graphics path 
    dir_path = os.path.dirname(dir_path) #data_analysis path 
    root_path = os.path.dirname(dir_path) #root path

    data_path = "{}\data".format(root_path) #works in data
    os.chdir(data_path)

    df_file_path = data_path + "\\merged_source_files.csv"
    df = pd.read_csv(df_file_path)
    
    #uses day, month, year columns of dataframe to get part of it regarding specified date
    dateDf = df[df['Day'] == day]
    dateDf = dateDf[dateDf['Month'] == month]
    dateDf = dateDf[dateDf['Year'] == year] 
    dateDf.reset_index(inplace = True, drop=True)

    return dateDf

def return_year(year): 
    '''
    Returns part of dateframe regarding requested year
    
    Parameters
    ----------
    year: string 
        Year - whose graph is required - as string 
    
    Returns
    -------
    pandas DataFrame 
        Part of DataFrame containing data regarding consumption on input year 
    '''

    real_path = os.path.realpath(__file__) #file path 
    dir_path = os.path.dirname(real_path) #graphics path
    dir_path = os.path.dirname(dir_path) #data_analysis path 
    root_path = os.path.dirname(dir_path) #root path 

    data_path = "{}\data".format(root_path) #works in data
    os.chdir(data_path)

    df_file_path = data_path + "\\merged_source_files.csv"
    df = pd.read_csv(df_file_path)

    yearDf = df[df['Year'] == year]
    yearDf.reset_index(inplace = True, drop=True)

    return yearDf


