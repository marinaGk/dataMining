import matplotlib.pyplot as plt
from numpy import size
import pandas as pd 
import os

def returns_stats(file_path): 

    file = pd.read_csv(file_path)
    del file['Time']
    sums = file.sum(axis = 1)
    max = sums.max()
    max_idx = sums.idxmax()
    min = sums.min()
    min_idx = sums.idxmin()
    avg = sums.mean()

    return sums, max, min, avg
    
def energy_per_day(date): 

    real_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(real_path)

    dir_path = dir_path[0:-4] + "sources\\"

    print(dir_path)

    os.chdir(dir_path)
    file_path = dir_path + date + ".csv"

    if ((os.stat(file_path).st_size == 0) == False): 

        file = pd.read_csv(file_path)

        time = file['Time']
        
        del file['Time']

        sums, max, min, avg = returns_stats(file_path)

        x = []

        for i in range(size(time)): 
            x.append(i)

        fig = plt.figure("Energy by day consumption")
        ax = fig.add_subplot()

        plt.xticks(x, time)

        ax.set_title("Total energy consumed throughout day, " + date[-2:] + "-" + date[-4:-2] + "-" + date[0:4])
        ax.set_xlabel("Time of day")
        ax.set_ylabel("Total energy")
        text = "Maximum energy consumed is: " + str(max) + "\nMinimum energy consumed is: " + str(min) + "\nAverage consumption is: " + str(round(avg, 2))
        fig.text(0, 0, text, bbox = dict(boxstyle="square,pad=0.3", fc="pink", ec="gray", lw=1))

        ax.scatter(x, sums, c = 'skyblue')

        for i, tick in enumerate(ax.get_xticklabels()): 
            if (i % 12 != 0): 
                tick.set_visible(False)

        mng = plt.get_current_fig_manager()
        mng.window.state('zoomed')

        plt.show()
