import matplotlib.pyplot as plt
from numpy import size
import pandas as pd
from dfPart import * 
from day_data import *
    
def make_day_dataframe(year, month, day): 

    file = return_day(year, month, day) #file is part of dataframe regarding specified date
    
    cols = ['Solar','Wind','Geothermal','Biomass','Biogas','Small hydro','Coal','Nuclear','Natural gas','Large hydro','Batteries','Imports','Other']

    file['Sums'] = file[cols].fillna(0).sum(axis = 1) #total energy used per day (all resources)

    return file

def energy_per_day(year, month, day): 
    '''Creates graph of energy used during specified date'''
    
    file = make_day_dataframe(year, month, day)

    x = []

    time = file['Time'] #time will be used as x-axis 

    sums = file['Sums']
    max = sums.max() #max energy measured (all resources)
    min = sums.min() #minimum energy measured (all resources)
    avg = sums.mean() #average energy consumed throughout day (all resources)

    #creates figure and plot
    fig = plt.figure("Energy by day consumption")
    ax = fig.add_subplot()
    ax.set_title("Total energy consumed throughout day, " + str(day) + "-" + str(month) + "-" + str(year))
    ax.set_xlabel("Time of day")
    ax.set_ylabel("Total energy")
    text = "Maximum energy consumed is: " + str(max) + "\nMinimum energy consumed is: " + str(min) + "\nAverage consumption is: " + str(round(avg, 2)) #left-bottom corner text 
    fig.text(0, 0, text, bbox = dict(boxstyle="square,pad=0.3", fc="pink", ec="gray", lw=1))

    for i in range(size(time)): 
        x.append(i) #makes an array of length equal to the amount of timestamps

    plt.xticks(x, time) #matches each tick on graph to each timestamp 

    ax.plot(x, sums, c = 'skyblue') #creates plot of points each one equal to a sum of energy at particular timestamp 

    for i, tick in enumerate(ax.get_xticklabels()): #only shows timestamps per one hour
        if (i % 12 != 0): 
            tick.set_visible(False)

    mng = plt.get_current_fig_manager() #makes figure full screen
    #mng.window.state('zoomed')

    plt.show()
