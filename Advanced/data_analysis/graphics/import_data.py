''' New data are being processed appropriately and are being imported into the databases

Requires python's numpy,pandas,os,sys libraries
and the code from the file "path.py" of the module "data_analysis" of the project folder and 
the functions merge_demands,merge_sourcesdata_merge from the files "merge_demand_files.py","merge_source_files.py","sources_and_demands.py" 
respectively which are on the folder preprocessing of the data_analysis module of the project.

'''

import os
import pandas as pd
from os import X_OK, listdir
from os.path import isfile, join
import numpy as np
import sys
from data_analysis.path import *

real_path = os.path.realpath(__file__)##path of the current file
real_path = resolve_path(real_path)
dir_path = os.path.dirname(real_path)##path of the current file
root_path = os.path.dirname(dir_path)
root_path = os.path.dirname(root_path)##path of the project

sys.path.append(root_path)
import data_analysis
from data_analysis.preprocessing.merge_demand_files import merge_demands
from data_analysis.preprocessing.merge_source_files import merge_sources
from data_analysis.preprocessing.sources_and_demands import data_merge
os.chdir(dir_path)

def insertfiles(filename):
    '''
    Here we insert the new files into the database. Remember the new files must be in the new data folder of the data folder of the project and must be have 
    a file for both sources and demands and they be a .csv type.#If these files are there and valid, we do some preprocessing and we insert the new data in the database.

    Parameters
    ----------
    filename:string
        Thats the name of the new folders that we want to add to the database 
    
    '''

    filename = filename + ".csv"

    real_path = os.path.realpath(__file__)##path of the current file
    dir_path = os.path.dirname(real_path)
    dir_path = os.path.dirname(dir_path)
    root_path = os.path.dirname(dir_path)##path of the project 

    os.chdir("{}\data\sources".format(root_path))##we get the files from the sources folder of the data folder of the project
    time_df = pd.read_csv("20190101.csv")##reading one of the files
    time = time_df['Time'].tolist()##array of timestamps

    sources_headers = ["Time","Solar","Wind","Geothermal","Biomass","Biogas","Small hydro","Coal","Nuclear","Natural gas","Large hydro","Batteries","Imports","Other"] ##prototype columns for a source file
    demands_headers = ["Time","Day ahead forecast","Hour ahead forecast","Current demand"] ##prototype columns for a demand file

    mypath="{}\data\processed_sources".format(root_path)##access to the processed_sources of the data folder 
    os.chdir(mypath)
    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]##get list of files from processed_sources
    mypath1="{}\data\\new_data\sources".format(root_path)##access to the sources of the new_data folder of data
    os.chdir(mypath1)
    sourcesfiles = [f for f in listdir(mypath1) if isfile(join(mypath1, f))]##get list of files from sources
    mypath2="{}\data\\new_data\demands".format(root_path)##access to the demands of the new_data folder of data
    os.chdir(mypath2)
    demandsfiles = [f for f in listdir(mypath2) if isfile(join(mypath2, f))]##get list of files from demands

    
    if (filename in sourcesfiles) and (filename in demandsfiles) and ("new_"+filename not in files):##Check if the files are already in the database and if the new files of a date are in the new_data folder
        ##If so
        os.chdir(mypath1)
        df1 = pd.read_csv(filename)##get the new file from new_data/sources
        col1=[]
        os.chdir(mypath2)
        df2 = pd.read_csv(filename)##get the new file from new_data/demands
        col2=[]
        for col in df1.columns:##get columns of both files
            col1.append(col)
        for col in df2.columns:
            col2.append(col)
        if len(df1)>200 and len(df2)>200 and col1 == sources_headers and col2 == demands_headers:##Check if the data for every file are over 200 and if the columns are the same with the prorotype
            
            mypath="{}\data\demand".format(root_path)##access to demand folder of the folder data of the project 
            os.chdir(mypath)
            df2.to_csv( "{}".format(filename), index=False, encoding='utf-8-sig')##put the selected file of the new_data/demands to the demand folder of data
            mypath="{}\data\sources".format(root_path )##access to sources folder of the folder data of the project 
            os.chdir(mypath)
            df1.to_csv( "{}".format(filename), index=False, encoding='utf-8-sig')#put the selected file of the new_data/sources to the sources folder of data

            merge_sources()##function called from the merge_sources_files.py
            merge_demands()##function called from the merge_demand_files.py
            data_merge()##function called from the sources_and_demands.py
            #Updates the merged_source_files.csv,merge_demand_files.csv and the merged_files.csv respectively
            

            list_tuples = []##list that saves the data of new file coming from new_data/sources
            ##Some preprocessing being done. 
            ##-If the number of the data are over 288, we delete the last data until we have 288
            ##-If data are missing, we add data from the previous timestamp that has data
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
            new_csv.to_csv( "new_{}.csv".format(filename[0:8]), index=False, encoding='utf-8-sig') ##The preprocessed file is saved in the processed_sources folder of data


              
            list_tuples = []##list that saves the data of new file coming from new_data/demands
            ##Some preprocessing being done. 
            ##-If the number of the data are over 288, we delete the last data until we have 288
            ##-If data are missing, we add data from the previous timestamp that has data
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
            new_csv.to_csv( "new_{}.csv".format(filename[0:8]), index=False, encoding='utf-8-sig')##The preprocessed file is saved in the processed_demands folder of data
            print("DONE")
        else:
            #If not
            print("The number of data are not enough for our application(must be over 200) or the columns of the files are not valid")

    else: 
        ##If not
        print("Something went wrong! The files that you are trying to import are arleady in the database or you don't have files for a day in sources and demands of the new_data folder")

    
    
