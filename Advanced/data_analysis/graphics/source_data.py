import matplotlib.pyplot as plt
from numpy import size
import pandas as pd 
import os
import numpy as np


directory=os.getcwd()
os.chdir(directory)

def returns_stats(array): 

    max = array.max()
    min = array.min()
    avg = array.mean()

    return max, min, avg


def source_per_day(source_index):
    visible = []
    options = ["Solar", "Wind", "Geothermal", "Biomass", "Biogas", "Small hydro", "Coal", "Nuclear", "Natural gas", "Large hydro", "Batteries", "Imports", "Other"]
    # real_path = os.path.realpath(__file__)
    # dir_path = os.path.dirname(real_path)
    dir_path = "{}/data".format(directory)
    os.chdir(dir_path)
    dir_path = dir_path + "\processed_sources\\"
    os.chdir(dir_path)
    Source_Data = []
    x=[]
    dates=[]
    counter=0
    for file in os.listdir():
        file_path = dir_path + file
        if ((os.stat(file_path).st_size == 0) == False) : 
            dates.append(file[8:10] + "-" + file[10:12])
            df = pd.read_csv(file_path)
            L=[]
            for i in range(len(df)):
                L.append(df.iloc[i,source_index+1])
            L = np.array(L)
            Source_Data.append(L.mean())
            x.append(counter)
            counter+=1
    Source_Data = np.array(Source_Data)
    avg = Source_Data.mean()
    max = Source_Data.max()
    min = Source_Data.min()

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

    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    plt.show()

