'''
Functions for checking the inputs of the user in the gui

Requires python's pandas,os libraries

'''

import os
import pandas as pd
directory=os.getcwd()

def checkTime(string):
    '''
    Function for checking if the Time is valid for the "outlier finder" feature

    Parameters
    ----------
    string:string
        The string is the time that the users inserts in the Outlier finder function
    
    Returns
    --------
    if the parameter is not compatible to the type it returns None
    else:
        if the string is not compatible to the form of time xx:00 it returns None
        else it returns the string

    '''
    try:   
        if len(string)==5 and int(string[0:2])>=0 and int(string[0:2])<=24 and string[3:5]=="00" and string[2]==":":
            return string
        else:
            return None
    except ValueError:
        return None


def checkFileName(filename):
    '''
    Function for checking if the Filename is valid for the "import data" feature. The name of the new files must be a type of date . For example 20220101.

    Parameters
    ----------
    filename:string
        The string is the time that the users inserts in the Outlier finder function
    
    Returns
    --------
    if the length of the parameter is <>8, or the type is not compatible it returns None
    else:
        if the parameters is not compatible to the form of date (e.g. 2022-01-01) it returns None
        else it returns the string

    '''
    if len(filename)>8 or len(filename)<8:
        return None
    else:
        string = filename[0:4]+"-"+filename[4:6]+"-"+filename[6:8]
        try:
            if len(string)==10 and int(string[0:4])>=2019 and int(string[5:7])>=0 and int(string[5:7])<=12 and int(string[8:10])>=0 and string[4]=="-" and string[7]=="-":
                if (int(string[5:7])==1 or int(string[5:7])==3 or int(string[5:7])==5 or int(string[5:7])==7 or int(string[5:7])==8 or int(string[5:7])==10 or int(string[5:7])==12) and int(string[8:10])<=31:
                    return string
                if (int(string[5:7])==4 or int(string[5:7])==6 or int(string[5:7])==9 or int(string[5:7])==11) and int(string[8:10])<=30:
                    return string
                if int(string[5:7])==2 and (int(string[0:4])%4==0 or int(string[0:4])%100!=0 or int(string[0:4])%400==0) and int(string[8:10])<=29:
                    return string
                if int(string[5:7])==2 and (int(string[0:4])%4!=0 or int(string[0:4])%100==0 or int(string[0:4])%400!=0) and int(string[8:10])<=28:
                    return string
                else:
                    print("This Date doesn't exist")
                    return None
        except ValueError:
            return None


def Years(file):
    '''
    Checks the years of our data

    Parameters
    -----------
    file:DataFrame
        the file is the DataFrame merged_files.csv of data folder

    Returns
    --------
    years:list
        List of unique years of our data

    '''
    years = file["Year"]
    years = pd.unique(years)
    return years

