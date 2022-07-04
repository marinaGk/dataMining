import pandas as pd 
import os

def merge_demands(): 
    '''Merges all demand files into one, required to make data processing faster'''

    real_path = os.path.realpath(__file__) #file path  
    dir_path = os.path.dirname(real_path) #preprocessing path 
    dir_path = os.path.dirname(dir_path) #data_analysis path 
    root_path = os.path.dirname(dir_path) #root path

    data_path = "{}\data".format(root_path) #works in data 
    demand_path = "{}\demand".format(data_path) #works in demand
    os.chdir(data_path) 

    filelist = []
    row_count = 0 
    days = []
    months = []
    years = []

    df = pd.DataFrame() #dataFrame to be used to store data 
    day_df = pd.DataFrame()

    for filename in os.listdir(demand_path): #for each file inside demand dir 
 
        file = demand_path + "/" + filename #gets name of file 

        if ((os.stat(file).st_size == 0) == False): #checks if file is empty

            day_df = pd.read_csv(file)
            day_df.drop(day_df.iloc[-1].name, inplace=True)

            #found out all demands files are 288 samples long so there's no need to delete/add records
            #if (row_count!=288) : print("not 288 lines" + filename)

            #works the same way as in sources to fix null entries
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

            #counts amount of rows per day in order to add its date same amount of times to 'Date' column on database
            #didn't try to make subrows since, either way, key for each row is both date and time
            row_count = len(day_df) 

            days = days + [filename[6:8]]*row_count
            months = months + [filename[4:6]]*row_count
            years = years + [filename[0:4]]*row_count

            filelist.append(day_df)

    df = pd.concat(filelist).reset_index(drop=True) #reads and concatenates all resource files into one dataframe 
    df.insert(0, 'Day', days) #adds day column
    df.insert(1, 'Month', months) #adds month column 
    df.insert(2, 'Year', years) #adds year column

    df.info()
    new_path = data_path + "\\merged_demand_files.csv" #saves in data
    df.to_csv(new_path, index=False)
