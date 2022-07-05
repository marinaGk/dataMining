''' 
It creates a graph in which the user can how energy fluctuates through the years 2019-2021 for the selected source 

Requires python's matplotlib,numpy,pandas,os,numpy libraries
and the code from the file "path.py" of the module "data_analysis" of the project folder.
'''


import matplotlib.pyplot as plt
from numpy import size
import pandas as pd 
import os
import numpy as np
from data_analysis.path import *

def returns_stats(array): 
    ''' 
    Function that returns the maximum value, the minimum value and the average value of an array of numbers 
    
    Parameters
    -----------
    array:list
        List of numbers 
        
    Returns
    --------
    max,min,avg:float
        Maximum,Minimum and Average Values of the array
    
    '''
    max = array.max()
    min = array.min()
    avg = array.mean()

    return max, min, avg


def source_per_day(source_index):
    '''
    Creates graph of energy for the selected source
    
    Parameters
    ----------
    source_index:int
        Index of the option that was selected (it refers to the list options)

    Result
    -------
    creation of a graph of energy for the selected in all the days of our database
    
    '''

    visible = []##keeps indices of visible ticks
    options = ["Solar", "Wind", "Geothermal", "Biomass", "Biogas", "Small hydro", "Coal", "Nuclear", "Natural gas", "Large hydro", "Batteries", "Imports", "Other"]##the options of sources that a user can select
    
    real_path = os.path.realpath(__file__)##path of current file 
    real_path = resolve_path(real_path)
    dir_path = os.path.dirname(real_path)
    dir_path = os.path.dirname(dir_path)
    root_path = os.path.dirname(dir_path)##root path of project
    
    dir_path = "{}/data".format(root_path)##we get to the data folder of the project
    os.chdir(dir_path)
    dir_path = dir_path + "\processed_sources\\"## we get data from the processed_sources folder
    os.chdir(dir_path)
    Source_Data = []##list in which we save the mean values of the selected source per day
    x=[]
    dates=[]##list of all days in database
    counter=0
    for file in os.listdir():##for every file in the processed_sources folder
        file_path = dir_path + file
        if ((os.stat(file_path).st_size == 0) == False) : 
            dates.append(file[8:10] + "-" + file[10:12])
            df = pd.read_csv(file_path)
            L=[]
            for i in range(len(df)):
                L.append(df.iloc[i,source_index+1])##Get data from the selected source
            L = np.array(L)## put it in array L
            Source_Data.append(L.mean())##calculate the mean value and put it in Source_Data list
            x.append(counter)
            counter+=1
    Source_Data = np.array(Source_Data)
    avg = Source_Data.mean()##average value of the Source_Data list
    max = Source_Data.max()##maximum value of the Source_Data list
    min = Source_Data.min()##minimum value of the Source_Data list

    ##Creation of graph 
    fig = plt.figure("Energy by year consumption")
    ax = fig.add_subplot()

    plt.xticks(x, dates)

    ax.set_title("Average energy consumption for, " + options[source_index])
    ax.set_xlabel("Date")
    ax.set_ylabel("Average energy per day")
    text = "Maximum energy consumed is: {:.2f}".format(max) + "\nMinimum energy consumed is: {:.2f}".format(min) + "\nAverage consumption is: {:.2f}".format(round(avg, 2))
    fig.text(0, 0, text, bbox = dict(boxstyle="square,pad=0.3", fc="pink", ec="gray", lw=1))

    ax.scatter(x, Source_Data, c = 'skyblue', marker='o')

    for i, tick in enumerate(ax.get_xticklabels()): 
        if i not in visible: 
            tick.set_visible(False)

    plt.show()

