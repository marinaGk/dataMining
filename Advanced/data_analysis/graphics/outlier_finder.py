''' 
Here we find days-outliers between hours of a day that are being selected by the user.Outlier is a day that its source's energy 
or demand's energy is more or less than the expected. The result is a graph in which we can the see data
and with clsutering methods(here we use DBSCAN) we determine the days-outliers

Requires python's matplotlib,numpy,pandas,os,numpy,sklearn,collections,plotly,math libraries
and the code from the file "path.py" of the module "data_analysis" of the project folder.

'''

import pandas as pd
from os import X_OK, listdir
from os.path import isfile, join
import os
from sklearn.cluster import DBSCAN
import numpy as np
from sklearn.datasets import make_friedman1
from sklearn.preprocessing import StandardScaler
from collections import Counter
from math import sqrt
import plotly.express as px
from data_analysis.path import *

def find_outliers(array):
    ''' 
    Function that calculates for every day in our database (from processed_sources and processed_demands of the data folder) and for all timestamps between the selected hours 
    some stats like mean value,variance and standard deviation for sources and demands and we save them in an array. From these stats we use the variance and we create a
    DataFrame with the variance of the sources and demands and we create a graph in order to see the values. Using the DBSCAN (clustering algorithm)
    we determine the outliers (for more information about DBSCAN and clustering you can see here: https://en.wikipedia.org/wiki/DBSCAN , https://en.wikipedia.org/wiki/Cluster_analysis)

    Parameters
    -----------
    array:list
        Hours the user selected for this process

    Returns
    --------
    graphs with data


    '''
    real_path = os.path.realpath(__file__)##path of current file 
    real_path = resolve_path(real_path)
    dir_path = os.path.dirname(real_path)
    dir_path = os.path.dirname(dir_path)
    root_path = os.path.dirname(dir_path)##root path of project

    dir_path = "{}\data\processed_sources".format(root_path)## we get data from the processed_sources of the data folder
    os.chdir(dir_path)

    files = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]##we get all the files from the processed_sources folder
    dates = [f[4:12] for f in listdir(dir_path) if isfile(join(dir_path, f))]##we get al the dates of the files from the processed_sources folder (every folder has as a name a date betwween the years 2019-2021)
    sources_headers = ["Time","Solar","Wind","Geothermal","Biomass","Biogas","Small hydro","Coal","Nuclear","Natural gas","Large hydro","Batteries","Imports","Other"]##prototype columns for a source file

    demands_headers = ["Time","Day ahead forecast","Hour ahead forecast","Current demand"]##prototype columns for a demand file

    stats_of_day_sources=[]##stats for every day in processed_sources
    stats_of_day_demands=[]##stats for every day in processed_demands

    sources_of_day=[]##data of day in processed_sources
    demands_of_day=[]##data of day in processed_demands

    df0 = pd.read_csv(files[0])##reading one of the files
    times = df0["Time"]##array of timestamps
    time = len(df0)#length of the times array

    k=array[0]##starting hour
    l=array[1]##ending hour
    for i in range(len(files)):#for every file in the processed_sources and demands we get the data from the starting hour until the ending hour and we calculate for every timestamp the sum of the data in every column  
        sources_of_day=[]##data of day in processed_sources
        demands_of_day=[]##data of day in processed_demands
        mypath="{}/data/processed_sources".format(root_path)##access to the processed_sources folder of the data folder
        os.chdir(mypath)
        df1 = pd.read_csv(files[i])
        for j in range(int(k*len(df1)/24),int(l*len(df1)/24)):
            total=0
            for x in range(1,len(sources_headers)):
                total+=df1.iloc[j,x]
            sources_of_day.append(total) ##data of day in processed_sources

        mypath="{}/data/processed_demands".format(root_path)##access to the processed_demands folder of the data folder
        os.chdir(mypath)
        df2 = pd.read_csv(files[i])
        for j in range(int(k*len(df2)/24),int(l*len(df2)/24)):
            total1=0
            for x in range(1,len(demands_headers)):
                total1+=df2.iloc[j,x]
            demands_of_day.append(total1)##data of day in processed_demands

        sources_of_day = np.array(sources_of_day)
        demands_of_day = np.array(demands_of_day)

        sources_mean = np.mean(sources_of_day)##mean value of day in processed_sources
        demands_mean = np.mean(demands_of_day)##mean value of day in processed_demands   

        sources_var = np.var(sources_of_day)##variance of day in processed_sources
        demands_var = np.var(demands_of_day)##variance of day in processed_demands  

        sources_std = np.std(sources_of_day)##standard deviation of day in processed_sources
        demands_std = np.std(demands_of_day)##standard deviation of day in processed_demands      

        stats_of_day_sources.append([sources_mean,sources_var,sources_std])##stats for every day in processed_sources
        stats_of_day_demands.append([demands_mean,demands_var,demands_std])##stats for every day in processed_demands

    x1 = str(k)##starting hour
    y1 = str(l)##ending hour
    ##Create compatible hours (type of xx:yy)
    start_time=""
    end_time=""
    if len(x1)==2:
        start_time = x1
    else:
        start_time = "0"+x1
    
    if len(y1)==2:
        end_time = y1
    else:
        end_time = "0"+y1
    scaler = StandardScaler() ##scaling method for data
    L=[]
    L1=[]
    ##For every stat per day we keep the variance in order to see the variance of the energy between the starting and ending hours
    for i in range(len(stats_of_day_sources)):
        L.append([files[i][4:12],stats_of_day_sources[i][1],stats_of_day_demands[i][1]])
        L1.append([stats_of_day_sources[i][1],stats_of_day_demands[i][1]])

    L2 = scaler.fit_transform(L1)##scaling of data 

    L3=[]##array of dates in form xxxx-yy-zz
    for i in range(len(L)):
        date=L[i][0]
        year=date[0:4]
        month = date[4:6]
        day = date[6:8]
        date = year + "-" + month + "-" + day
        L3.append([date,L2[i][0],L2[i][1]])


    X =  pd.DataFrame(L2,columns=["Sources","Demands"])
    X1 = pd.DataFrame(L3,columns=["Date","Sources","Demands"])

    ##graph of data
    fig = px.scatter(X1,x="Sources",y="Demands",hover_name="Date",labels={
        "Sources":"Variance of Sources",
        "Demands":"Variance of Demands"
    },
    title="Sources vs Demands for hours betweeen {}:00-{}:00".format(start_time,end_time)
    )
    fig.show()

    ##Here is where the DBSCAN algorith takes place. DBSCAN requires two parameters: the minimum number of points required to form a dense region[a] (minPts) and eps which
    ##is the maximum distance between the points of a dense. The result is outliers are not getting in any cluster and we get them pretty easily
    num=input("Enter number of minimum samples in DBSCAN:")
    distance=input("Enter eps of DBScan:")

    try:##check if the user put compatible values
        minsamples=int(num)
        
        distance=float(distance)

        ##DBSCAN happens
        dbscan=DBSCAN(eps=distance,min_samples=minsamples)
        dbscan_clusters=dbscan.fit_predict(X)##every point is in a specific cluster
        print ("DBSCAN",Counter(dbscan.labels_))

        X["cluster"]=dbscan_clusters
        dbscanscluster_values=sorted(X['cluster'].unique())

        X["Date"] = X1["Date"]
        outliers=[]#Outliers are in cluster "-1". So we print only the dates that their stats are in this cluster.
        Cluster_name=[]
        for i in range(len(X)):
            if X["cluster"][i]==-1:
                outliers.append(X["Date"][i])
                Cluster_name.append("outlier")
            else:
                Cluster_name.append("cluster {}".format(X["cluster"][i]))
        X["cluster-name"]=Cluster_name

        if len(outliers)>0:
            days=','.join([str(elem) for elem in outliers])
            print("DBSCAN: Outliers for {}.".format(days))
        else:
            print("DBSCAN: No outliers")

        ##graphs that shows the clustering that happened
        fig = px.scatter(X,x="Sources",y="Demands",hover_name="Date",color="cluster-name",labels={
            "Sources":"Variance of Sources",
            "Demands":"Variance of Demands",
            "cluster":"Clusters"
        },
        title="Sources vs Demands for hours betweeen {}:00-{}:00".format(start_time,end_time)
        )
        fig.show()
        return "GOOD"
    except ValueError:##if the values are not compatible
        print("Wrong Input")
    except KeyboardInterrupt:##If the process is interrupted
        print("Process interrupted")




