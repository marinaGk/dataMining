import pandas as pd 
import os

directory=os.getcwd()
os.chdir(directory)

def return_day(year, month, day): 
    '''Returns part of dataframe regarding requested date'''

    real_path = os.path.realpath(__file__) #file path
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
    '''Returns part of dateframe regarding requested year'''

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


