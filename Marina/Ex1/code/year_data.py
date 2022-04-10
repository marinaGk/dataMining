import csv
import matplotlib
import matplotlib.pyplot as plt
import os

from day_data import *

def energy_per_year(year):

    counter = 0
    x = []
    visible = []
    dates = []
    average = pd.Series([])

    real_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(real_path)

    dir_path = dir_path[0:-4] + "sources\\"

    os.chdir(dir_path)

    for file in os.listdir():
        file_path = dir_path + file
        if ((os.stat(file_path).st_size == 0) == False and file.startswith(year)) : 
            
            x.append(counter)
            if (file[6:8] == "01"): visible.append(counter)

            counter += 1

            date = file[0:8]
            dates.append(file[6:8] + "-" + file[4:6])

            sums, max, min, avg = returns_stats(file_path)
            average = pd.concat([average, pd.Series([round(avg, 2)])])

    max = average.max()
    min = average.min()
    avg = average.mean()

    fig = plt.figure("Energy by year consumption")
    ax = fig.add_subplot()

    plt.xticks(x, dates)

    ax.set_title("Average energy consumption throughout year, " + year)
    ax.set_xlabel("Date")
    ax.set_ylabel("Average energy per day")
    text = "Maximum energy consumed is: " + str(max) + "\nMinimum energy consumed is: " + str(min) + "\nAverage consumption is: " + str(round(avg, 2))
    fig.text(0, 0, text, bbox = dict(boxstyle="square,pad=0.3", fc="pink", ec="gray", lw=1))

    ax.scatter(x, average, c = 'skyblue')

    for i, tick in enumerate(ax.get_xticklabels()): 
        if i not in visible: 
            tick.set_visible(False)

    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')

    plt.show()
