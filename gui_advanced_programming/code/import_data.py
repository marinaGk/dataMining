import os
import pandas as pd
from os import X_OK, listdir
from os.path import isfile, join
import numpy as np


directory=os.getcwd()

def insertfiles(filename):
    print(filename)
    filename = filename + ".csv"

    os.chdir("{}/sources".format(directory))
    time_df = pd.read_csv("20190101.csv")
    time = time_df['Time'].tolist()

    sources_headers = ["Time","Solar","Wind","Geothermal","Biomass","Biogas","Small hydro","Coal","Nuclear","Natural gas","Large hydro","Batteries","Imports","Other"]
    demands_headers = ["Time","Day ahead forecast","Hour ahead forecast","Current demand"]



    mypath1="{}/new_data/sources".format(directory)
    os.chdir(mypath1)
    sourcesfiles = [f for f in listdir(mypath1) if isfile(join(mypath1, f))]
    print(sourcesfiles)
    mypath2="{}/new_data/demands".format(directory)
    os.chdir(mypath2)
    demandsfiles = [f for f in listdir(mypath2) if isfile(join(mypath2, f))]
    print(demandsfiles)
    if (filename in sourcesfiles) and (filename in demandsfiles):
        print("GOOD")
        os.chdir(mypath1)
        df1 = pd.read_csv(filename)
        os.chdir(mypath2)
        df2 = pd.read_csv(filename)
        
        if len(df1)>150 and len(df2)>150:
            print("GOOD GOOD")

            os.chdir("{}/code".format(directory))
            df = pd.read_csv("merged_source_files.csv")
            
            filelist=[]
            days = []
            months = []
            years = []

            day_df = df1

            row_count = len(day_df) #counts amount of rows per day in order to add its date the same amount of times to 'Date' column on dataFrame
            #didn't try to make subrows since, either way, key for each row is both date and time

            if ("Natural Gas" in day_df.columns) :
                day_df.rename(columns = {'Natural Gas':'Natural gas'}, inplace = True)
            if ("Large Hydro" in day_df.columns):
                day_df.rename(columns = {'Large Hydro':'Large hydro'}, inplace = True)

            if(row_count > 288):
                day_df.drop(day_df.iloc[-1].name, inplace=True)
                row_count = len(day_df)

            if(row_count < 288): 
                count = 288 - row_count
                last_time = day_df['Time'].iloc[-1]

                for i in range(count):
                    day_df = day_df.append(day_df.iloc[row_count-1+i], ignore_index=True)
                    day_df['Time'].iloc[-1] = time[row_count+i]
                row_count = len(day_df)
            
            nulls = []
            cols = ['Solar', 'Wind', 'Geothermal', 'Biomass', 'Biogas', 'Small hydro', 'Coal', 'Nuclear', 'Natural gas', 'Large hydro', 'Batteries', 'Imports', 'Other']
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

                #if (len(nulls)!=0): print(nulls)

            day_df['Sums'] = day_df[cols].sum(axis = 1) #total energy used per day (all resources)
            average = day_df['Sums'].mean()
            day_df['Sums average'] = round(average, 1)
            renewable_cols = ['Solar', 'Wind', 'Geothermal', 'Biomass', 'Biogas', 'Small hydro', 'Large hydro', 'Batteries']
            day_df['Renewable sums'] = day_df[renewable_cols].sum(axis=1)

            days = days + [filename[6:8]]*row_count
            months = months + [filename[4:6]]*row_count
            years = years + [filename[0:4]]*row_count

            filelist.append(day_df)
            
            df3 = pd.concat(filelist).reset_index(drop=True) #reads and concatenates all resource files into one dataframe 
            df3.insert(0, 'Day', days) #adds day column
            df3.insert(1, 'Month', months) #adds month column 
            df3.insert(2, 'Year', years) #adds year column

            df_sources_new = pd.concat([df,df3])
            os.chdir("{}/code".format(directory))
            df_sources_new.to_csv("merged_source_files.csv", index=False)


            os.chdir("{}/code".format(directory))
            df = pd.read_csv("merged_demand_files.csv")

            filelist=[]
            days = []
            months = []
            years = []

            day_df = df2
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

            df3 = pd.concat(filelist).reset_index(drop=True) #reads and concatenates all resource files into one dataframe 
            df3.insert(0, 'Day', days) #adds day column
            df3.insert(1, 'Month', months) #adds month column 
            df3.insert(2, 'Year', years) #adds year column

            df_demands_new = pd.concat([df,df3])
            os.chdir("{}/code".format(directory))
            df_demands_new.to_csv("new_merged_demand_files.csv", index=False)

            #Merge of files of sources and demands
            cols = ['Day ahead forecast', 'Hour ahead forecast', 'Current demand']
            for i in cols: 
                column = df_demands_new[i].tolist()
                df_sources_new[i] = column

            df_sources_new.to_csv("merged_files.csv", index=False)

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
            mypath="{}/processed_sources".format(directory)
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
            mypath="{}/processed_demands".format(directory)
            os.chdir(mypath)
            new_csv = pd.DataFrame(list_tuples)
            new_csv.columns = demands_headers
            new_csv.to_csv( "new_{}.csv".format(filename[0:8]), index=False, encoding='utf-8-sig')
            print("DONE")
        else:
            print("NOT GOOD GOOD")

    else: 
        print("NOT GOOD")

    
    




