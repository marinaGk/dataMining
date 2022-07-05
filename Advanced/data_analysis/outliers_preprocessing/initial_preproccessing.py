'''
Here we preprocessing the data of the folders sources and demands, so that the data of energy sources and demands are ready for analysis. The preprocessed data are 
saved in the processed_sources and processed_demands respectively and they are used for finding outliers 

Requires python's numpy,pandas,os libraries

'''


import pandas as pd
from os import X_OK, listdir
from os.path import isfile, join
import os
import numpy as np

print("SOURCES")
real_path = os.path.realpath(__file__)##path of the current file
dir_path = os.path.dirname(real_path)
dir_path = os.path.dirname(dir_path)
root_path = os.path.dirname(dir_path)##path of the project
mypath="{}\data\sources".format(root_path)##access to the sources folder of the data folder of the project
os.chdir(mypath)

df=pd.read_csv("20190101.csv")##reading one of the files
time=df["Time"]##array of timestamps

sourcesfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]##get list of files from sources

sources_headers = ["Time","Solar","Wind","Geothermal","Biomass","Biogas","Small hydro","Coal","Nuclear","Natural gas","Large hydro","Batteries","Imports","Other"]##prototype columns for a source file

for x in range(len(sourcesfiles)):#for every file in the sources folder
    ##We do some preprocessing.
    ##-If the number of the data are over 288, we delete the last data until we have 288
    ##-If data are missing, we add data from the previous timestamp that has data
   try:
       mypath="{}\data\sources".format(root_path)
       os.chdir(mypath)
       list_tuples = []
       df1 = pd.read_csv(sourcesfiles[x])
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
       new_csv.to_csv("new_{}.csv".format(sourcesfiles[x][0:8]), index=False, encoding='utf-8-sig')##The preprocessed file is saved in the processed_sources folder of data
   except:
       continue

print("DEMANDS")
mypath="{}\data\demand".format(root_path)##access to the demands folder of the data folder of the project
os.chdir(mypath)

demandfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]##get list of files from demands

demands_headers = ["Time","Day ahead forecast","Hour ahead forecast","Current demand"]##prototype columns for a source file

for x in range(len(demandfiles)):#for every file in the demand folder
    ##We do some preprocessing.
    ##-If the number of the data are over 288, we delete the last data until we have 288
    ##-If data are missing, we add data from the previous timestamp that has data
   try:
       mypath="{}\data\demand".format(root_path)
       os.chdir(mypath)
       list_tuples = []
       df1 = pd.read_csv(demandfiles[x])
       for j in range(len(df1)):
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
       if len(time)>len(df1):
           for l in range(len(time)-len(df1)):
               d=[]
               d.append(time[len(df1)+l])
               for z in range(1,len(demands_headers)):
                   d.append(list_tuples[-1][z])
               list_tuples.append(d)
       mypath="{}\data\processed_demands".format(root_path)
       os.chdir(mypath)
       new_csv = pd.DataFrame(list_tuples)
       new_csv.columns = demands_headers
       new_csv.to_csv( "new_{}.csv".format(demandfiles[x][0:8]), index=False, encoding='utf-8-sig')##The preprocessed file is saved in the processed_demands folder of data
   except:
       continue

