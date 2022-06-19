import matplotlib.pyplot as plt
from numpy import float64
import pandas as pd
from dfPart import * 
from day_data import *

def energy_per_year(year):
    '''Creates graph of energy used during specified year'''

    x = []
    visible = [] #keeps indices of visible ticks
    dates = [] #keeps dates of year to be used as ticks in graph
    counter = 0 #keeps count of amount of days in year
    average = pd.Series([], dtype='float64') #keeps average energy usage per day throughout year

    file = return_year(year) #file is part of dataframe regarding specified year 

    for idx, row in file.iterrows(): 

        if (idx%288 == 0): #beginning of day

            counter+=1 
            date = str(row['Day']) + "-" + str(row['Month'])
            dates.append(date) 
            
            if(row['Day'] == 1): #beginning of month - only visible ticks
                visible.append(idx/288)

            avg = row['Sums average']
            average = pd.concat([average, pd.Series([avg])])

    max = average.max()
    min = average.min()
    avg = average.mean()

    #creates figure and plot
    fig = plt.figure("Energy by year consumption")
    ax = fig.add_subplot()
    ax.set_title("Average energy consumption throughout year, " + str(year))
    ax.set_xlabel("Date")
    ax.set_ylabel("Average energy per day")
    text = "Maximum energy consumed is: " + str(max) + "\nMinimum energy consumed is: " + str(min) + "\nAverage consumption is: " + str(round(avg, 2))
    fig.text(0, 0, text, bbox = dict(boxstyle="square,pad=0.3", fc="pink", ec="gray", lw=1))

    for i in range(counter):
        x.append(i) #makes array of length equal to amount of days in year

    plt.xticks(x, dates) #matches each tick on graph to each date

    ax.plot(x, average, c = 'skyblue') #creates plot of points each one equal to average energy at particular date 

    for i, tick in enumerate(ax.get_xticklabels()): #only shows dates at beggining of month 
        if i not in visible: 
            tick.set_visible(False)

    mng = plt.get_current_fig_manager() #makes figure full screen
    #mng.window.state('zoomed')

    plt.show()