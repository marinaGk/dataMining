'''for one file only, instead of for looping, getting for each row its sum in a series 
then plot against time'''


import csv
from time import time_ns
import matplotlib.pyplot as plt
import matplotlib.axis as axes
from numpy import size
import pandas as pd 


def sources_per_day(): 

    file = pd.read_csv('Ex1/sources/20190101.csv')

    time = file['Time']
    
    del file['Time']

    index = file.index.values

    sums = file.sum(axis = 1)

    x = []

    for i in range(size(time)): 
        x.append(i)

    fig, ax = plt.subplots()

    plt.xticks(x, time)

    ax.plot(x, sums)

    for i, tick in enumerate(ax.get_xticklabels()): 
        if (i % 24 != 0): 
            tick.set_visible(False)
        print(i)

    plt.show()

sources_per_day()
