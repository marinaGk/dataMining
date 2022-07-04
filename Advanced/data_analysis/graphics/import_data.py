import os
import pandas as pd
from os import X_OK, listdir
from os.path import isfile, join
import numpy as np


##Inserting a file into the database, means also that you already have a file for demands and soucres in the new_data folder with the same name <date>.csv.
##If these files are there and valid, we do some preprocessing and we insert the new data in the database.

def insertfiles(filename):
    filename = filename + ".csv"

    real_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(real_path)
    dir_path = os.path.dirname(dir_path)
    root_path = os.path.dirname(dir_path)

    os.chdir("{}\data\sources".format(root_path))
    time_df = pd.read_csv("20190101.csv")
    time = time_df['Time'].tolist()

    sources_headers = ["Time","Solar","Wind","Geothermal","Biomass","Biogas","Small hydro","Coal","Nuclear","Natural gas","Large hydro","Batteries","Imports","Other"]
    demands_headers = ["Time","Day ahead forecast","Hour ahead forecast","Current demand"]

    mypath="{}\data\processed_sources".format(root_path)
    os.chdir(mypath)
    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    mypath1="{}\data\\new_data\sources".format(root_path)
    os.chdir(mypath1)
    sourcesfiles = [f for f in listdir(mypath1) if isfile(join(mypath1, f))]
    mypath2="{}\data\\new_data\demands".format(root_path)
    os.chdir(mypath2)
    demandsfiles = [f for f in listdir(mypath2) if isfile(join(mypath2, f))]

    ##Check if the files are already in the database and if the files of a date are in their folders
    
    if (filename in sourcesfiles) and (filename in demandsfiles) and ("new_"+filename not in files):
        os.chdir(mypath1)
        df1 = pd.read_csv(filename)
        col1=[]
        os.chdir(mypath2)
        df2 = pd.read_csv(filename)
        col2=[]
        for col in df1.columns:
            col1.append(col)
        for col in df2.columns:
            col2.append(col)
        if len(df1)>200 and len(df2)>200 and col1 == sources_headers and col2 == demands_headers:
            
            ##Here is where the preprocessing happens 

            mypath="{}\data\demand".format(root_path )
            os.chdir(mypath)
            df2.to_csv( "{}".format(filename), index=False, encoding='utf-8-sig')
            mypath="{}\data\sources".format(root_path )
            os.chdir(mypath)
            df1.to_csv( "{}".format(filename), index=False, encoding='utf-8-sig')

            merge_sources()
            merge_demands()
            data_merge()

            #New file in processed_sources
            list_tuples = []
            for j in range(len(df1)):
                if j==len(time):
                    continue
                d=[]
                d.append(time[j])
                for z in range(1,len(sources_headers)):
                    if np.isnan(df1.iloc[j,z])==True:
                        if np.isnan(df1.iloc[0,z])==True:
                            d.append(0)
                        else:
                            d.append(list_tuples[-1][z])
                    else:
                        d.append(df1.iloc[j,z])
                list_tuples.append(d)
            if len(time)>len(df1):
                for l in range(len(time)-len(df1)):
                    d=[]
                    d.append(time[len(df1)+l])
                    for z in range(1,len(sources_headers)):
                        d.append(list_tuples[-1][z])
                    list_tuples.append(d)
            mypath="{}\data\processed_sources".format(root_path)
            os.chdir(mypath)
            new_csv = pd.DataFrame(list_tuples)
            new_csv.columns = sources_headers
            new_csv.to_csv( "new_{}.csv".format(filename[0:8]), index=False, encoding='utf-8-sig')


            #New file in processed_demands     
            list_tuples = []
            for j in range(len(df2)):
                if j==len(time):
                    continue
                d=[]
                d.append(time[j])
                for z in range(1,len(demands_headers)):
                    if np.isnan(df1.iloc[j,z])==True:
                        if np.isnan(df1.iloc[0,z])==True:
                            d.append(0)
                        else:
                            d.append(list_tuples[-1][z])
                    else:
                        d.append(df1.iloc[j,z])
                list_tuples.append(d)
            if len(time)>len(df2):
                for l in range(len(time)-len(df1)):
                    d=[]
                    d.append(time[len(df1)+l])
                    for z in range(1,len(demands_headers)):
                        d.append(list_tuples[-1][z])
                    list_tuples.append(d)
            mypath="{}\data\processed_demands".format(root_path )
            os.chdir(mypath)
            new_csv = pd.DataFrame(list_tuples)
            new_csv.columns = demands_headers
            new_csv.to_csv( "new_{}.csv".format(filename[0:8]), index=False, encoding='utf-8-sig')
            print("DONE")
        else:
            print("The number of data are not enough for our application(must be over 200) or the columns of the files are not valid")

    else: 
        print("Something went wrong! The files that you are trying to import are arleady in the database or you don't have files for a day in sources and demands of the new_data folder")

    
    
def merge_sources(): 
    '''Merges all source files into one, required to make data processing faster'''
    
    real_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(real_path)
    dir_path = os.path.dirname(dir_path)
    root_path = os.path.dirname(dir_path)

    data_path = "{}\data".format(root_path)
    source_path = "{}\sources".format(data_path)
    os.chdir(source_path) 

    filelist = []
    row_count = 0 
    days = []
    months = []
    years = []

    df = pd.DataFrame() #dataFrame to be used to store data 
    day_df = pd.DataFrame()

    time_df = pd.read_csv(source_path + "/20190101.csv") #reads sample times from one of the files 
    time = time_df['Time'].tolist()

    for filename in os.listdir(source_path):

        file = source_path + "/" + filename

        if ((os.stat(file).st_size == 0) == False):

            day_df = pd.read_csv(file)

            #counts amount of rows per day in order to add its date the same amount of times to 'Date' column on dataFrame
            #didn't try to make subrows since, either way, key for each row is both date and time
            row_count = len(day_df) 

            #fixes naming issues
            if ("Natural Gas" in day_df.columns) :
                day_df.rename(columns = {'Natural Gas':'Natural gas'}, inplace = True)
            if ("Large Hydro" in day_df.columns):
                day_df.rename(columns = {'Large Hydro':'Large hydro'}, inplace = True)

            #drops repetition of 00:00
            if(row_count > 288):
                day_df.drop(day_df.iloc[-1].name, inplace=True)
                row_count = len(day_df)

            #if there's missing samples, makes new row and adds to it time according to the time array created before, leaving the rest of the rows empty
            if(row_count < 288): 
                count = 288 - row_count

                for i in range(count):
                    day_df = day_df.append(day_df.iloc[row_count-1+i], ignore_index=True)
                    day_df['Time'].iloc[-1] = time[row_count+i]
                row_count = len(day_df)

            #fills null samples
            nulls = []
            cols = ['Solar', 'Wind', 'Geothermal', 'Biomass', 'Biogas', 'Small hydro', 'Coal', 'Nuclear', 'Natural gas', 'Large hydro', 'Batteries', 'Imports', 'Other']
            for i in cols:
                nulls = day_df[day_df[i].isnull()].index.tolist() #makes nulls array contain indices of null samples for each column
                for j in nulls: 
                    if (len(nulls) == row_count) : 
                        day_df[i].loc[j] = 0 #if entire column is null, set to zero 
                    elif (j==0): 
                        #first null sample is given the value of next sample
                        #if it's also the first sample of database, it's appended in nulls list so that it will be fixed after all the others
                        if(nulls.index(j) == 0): 
                            nulls.append(j) 
                        else :
                            day_df[i].loc[j] = day_df[i].loc[j+1]
                    else:
                        day_df[i].loc[j] = day_df[i].loc[j-1] #null samples take value of previous sample

            day_df['Sums'] = day_df[cols].sum(axis = 1) #total energy used per five minutes for all resources
            average = day_df['Sums'].mean() #average of enegry sums for day 
            day_df['Sums average'] = round(average, 1)
            renewable_cols = ['Solar', 'Wind', 'Geothermal', 'Biomass', 'Biogas', 'Small hydro', 'Large hydro', 'Batteries']
            day_df['Renewable sums'] = day_df[renewable_cols].sum(axis=1) #total renewable energy used per five minutes
            day_df['Day sum'] = day_df['Sums'].sum() #total energy consumed in a day

            #used to create day, month and year columns
            #adds to list current day, month and year for each five minute record 
            days = days + [filename[6:8]]*row_count 
            months = months + [filename[4:6]]*row_count
            years = years + [filename[0:4]]*row_count

            filelist.append(day_df)

    df = pd.concat(filelist).reset_index(drop=True) #reads and concatenates all resource files into one dataframe 
    df.insert(0, 'Day', days) #adds day column
    df.insert(1, 'Month', months) #adds month column 
    df.insert(2, 'Year', years) #adds year column
    
    new_path = data_path + "\\merged_source_files.csv"
    df.info()
    df.to_csv(new_path, index=False)



def merge_demands(): 
    '''Merges all demand files into one, required to make data processing faster'''
    
    real_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(real_path)
    dir_path = os.path.dirname(dir_path)
    root_path = os.path.dirname(dir_path)

    data_path = "{}\data".format(root_path)
    demand_path = "{}\demand".format(data_path)
    os.chdir(data_path) 

    filelist = []
    row_count = 0 
    days = []
    months = []
    years = []

    df = pd.DataFrame() #dataFrame to be used to store data 
    day_df = pd.DataFrame()

    for filename in os.listdir(demand_path):

        file = demand_path + "/" + filename

        if ((os.stat(file).st_size == 0) == False):

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
    new_path = data_path + "\\merged_demand_files.csv"
    df.to_csv(new_path, index=False)


def data_merge(): 
    '''Makes file containing both sources and demands records'''

    real_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(real_path)
    dir_path = os.path.dirname(dir_path)
    root_path = os.path.dirname(dir_path)

    data_path = "{}\data".format(root_path)
    os.chdir(data_path) 

    demands_file = data_path + "\\merged_demand_files.csv"
    sources_file = data_path + "\\merged_source_files.csv"

    demands_df = pd.read_csv(demands_file)
    sources_df = pd.read_csv(sources_file)

    cols = ['Day ahead forecast', 'Hour ahead forecast', 'Current demand']
    for i in cols: 
        column = demands_df[i].tolist()
        sources_df[i] = column

    new_path = data_path + "\\merged_files.csv"
    sources_df.info()
    sources_df.to_csv(new_path, index=False)



