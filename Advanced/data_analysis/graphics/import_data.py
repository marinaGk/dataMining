import os
import pandas as pd
from os import X_OK, listdir
from os.path import isfile, join
import numpy as np
import sys
from data_analysis.path import *

real_path = os.path.realpath(__file__)
real_path = resolve_path(real_path)
dir_path = os.path.dirname(real_path)
root_path = os.path.dirname(dir_path)
root_path = os.path.dirname(root_path)

sys.path.append(root_path)
import data_analysis
from data_analysis.preprocessing.merge_demand_files import merge_demands
from data_analysis.preprocessing.merge_source_files import merge_sources
from data_analysis.preprocessing.sources_and_demands import data_merge

os.chdir(dir_path)

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

    
    
