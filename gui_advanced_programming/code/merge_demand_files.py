import pandas as pd 
import os

def merge_demands(): 

    real_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(real_path)
    dir_path = dir_path + "\demand\\"
    os.chdir(dir_path) #works inside data directory (sources)

    filelist = []
    row_count = 0 
    days = []
    months = []
    years = []

    df = pd.DataFrame() #dataFrame to be used to store data 
    day_df = pd.DataFrame()

    for filename in os.listdir(dir_path):

        file = dir_path + filename

        if ((os.stat(file).st_size == 0) == False):

            day_df = pd.read_csv(file)
            day_df.drop(day_df.iloc[-1].name, inplace=True)

            nulls = []
            cols = ['Day ahead forecast', 'Hour ahead forecast', 'Current demand']
            for i in cols: 
                nulls = day_df[day_df[i].isnull()].index.tolist()
                for j in nulls: 
                    if (len(nulls) == row_count) : 
                        day_df[i].loc[j] = 0
                    elif (j==0): 
                        if(nulls.index(j) == 0): 
                            nulls.append(j)
                        else :
                            day_df[i].loc[j] = day_df[i].loc[j+1]
                    else:
                        day_df[i].loc[j] = day_df[i].loc[j-1]

            row_count = len(day_df) #counts amount of rows per day in order to add its date same amount of times to 'Date' column on database
            #didn't try to make subrows since, either way, key for each row is both date and time

            if (row_count!=288) : print(filename)

            days = days + [filename[6:8]]*row_count
            months = months + [filename[4:6]]*row_count
            years = years + [filename[0:4]]*row_count

            filelist.append(day_df)

    df = pd.concat(filelist).reset_index(drop=True) #reads and concatenates all resource files into one dataframe 
    df.insert(0, 'Day', days) #adds day column
    df.insert(1, 'Month', months) #adds month column 
    df.insert(2, 'Year', years) #adds year column

    df.info()
    new_path = os.path.dirname(real_path) + "\\merged_demand_files.csv"
    df.to_csv(new_path, index=False)

merge_demands()