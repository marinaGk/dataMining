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


directory=os.getcwd()
print(directory)
##Here we find the days-outliers of our database. Days that their demand or supplement of energy is more or less than usual. Important 
##if we want to see if there are wrong data in a day. 


#Για τα επεξεργασμένα αρχεία των φακέλων processed_sources και processed_demands βρίσκουμε για τις ζητούμενες χρονικές στιγμές το άθροισμα
#της ενέργειας και επιπλέον βρίσκουμε για κάθε ημέρα στατιστικά στοιχεία όπως η μέση τιμή,η διακύμανση και η τυπική απόκλιση.
##Κάνουμε unzip το αρχείο data.zip για να εκτελέσουμε μονο το ακόλουθο κομμάτι κώδικα

def find_outliers(array):
    
    dir_path = "{}/data/processed_sources".format(directory)
    os.chdir(dir_path)

    files = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
    dates = [f[4:12] for f in listdir(dir_path) if isfile(join(dir_path, f))]
    sources_headers = ["Time","Solar","Wind","Geothermal","Biomass","Biogas","Small hydro","Coal","Nuclear","Natural gas","Large hydro","Batteries","Imports","Other"]

    demands_headers = ["Time","Day ahead forecast","Hour ahead forecast","Current demand"]

    stats_of_day_sources=[]
    stats_of_day_demands=[]

    sources_of_days=[]
    demands_of_days=[]

    sources_of_day=[]
    demands_of_day=[]

    df0 = pd.read_csv(files[0])
    times = df0["Time"]
    time = len(df0)

    k=array[0]
    l=array[1]
    for i in range(len(files)):
        sources_of_day=[]
        demands_of_day=[]
        mypath="{}/data/processed_sources".format(directory)
        os.chdir(mypath)
        df1 = pd.read_csv(files[i])
        for j in range(int(k*len(df1)/24),int(l*len(df1)/24)):
            total=0
            for x in range(1,len(sources_headers)):
                total+=df1.iloc[j,x]
            sources_of_day.append(total) 

        mypath="{}/data/processed_demands".format(directory)
        os.chdir(mypath)
        df2 = pd.read_csv(files[i])
        for j in range(int(k*len(df2)/24),int(l*len(df2)/24)):
            total1=0
            for x in range(1,len(demands_headers)):
                total1+=df2.iloc[j,x]
            demands_of_day.append(total1)

        sources_of_day = np.array(sources_of_day)
        demands_of_day = np.array(demands_of_day)

        sources_mean = np.mean(sources_of_day)
        demands_mean = np.mean(demands_of_day)     

        sources_var = np.var(sources_of_day)
        demands_var = np.var(demands_of_day)     

        sources_std = np.std(sources_of_day)
        demands_std = np.std(demands_of_day)     

        stats_of_day_sources.append([sources_mean,sources_var,sources_std])
        stats_of_day_demands.append([demands_mean,demands_var,demands_std])

##Στην συνέχεια, αφού κάνουμε scale τα δεδομένα, δημιουργούμε ένα DataFrame όπου κάθε ημέρα χαρακτηρίζεται από την διακύμανση της ενέργειας που υπάρχει 
##στα sources και τη διακύμανση της ενέργειας που υπάρχει στα demands. Έχοντας κάνει αυτό, μπορούμε να αναπαραστήσουμε τα δεδομένα σε μια γραφική παράσταση
##Sources vs Demands

    x1 = str(k)
    y1 = str(l)
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
    scaler = StandardScaler()
    L=[]
    L1=[]
    for i in range(len(stats_of_day_sources)):
        L.append([files[i][4:12],stats_of_day_sources[i][1],stats_of_day_demands[i][1]])
        L1.append([stats_of_day_sources[i][1],stats_of_day_demands[i][1]])

    L2 = scaler.fit_transform(L1)

    L3=[]
    for i in range(len(L)):
        date=L[i][0]
        year=date[0:4]
        month = date[4:6]
        day = date[6:8]
        date = year + "-" + month + "-" + day
        L3.append([date,L2[i][0],L2[i][1]])


    X =  pd.DataFrame(L2,columns=["Sources","Demands"])
    X1 = pd.DataFrame(L3,columns=["Date","Sources","Demands"])

    # colormap=['b','g','r','c','m','y','k','slateblue','springgreen','indigo','teal','lightcoral','gold']

    fig = px.scatter(X1,x="Sources",y="Demands",hover_name="Date",labels={
        "Sources":"Variance of Sources",
        "Demands":"Variance of Demands"
    },
    title="Sources vs Demands for hours betweeen {}:00-{}:00".format(start_time,end_time)
    )
    fig.show()

##Ένας αποδοτικός αλγόριθμος για την έυρεση των outliers είναι ο DBSCAN. Βάζοντας κατάλληλες παραμέτρους min_samples και eps, μπορούμε να βρούμε
##τις ημέρες εκείνες που η ζήτηση ή η παραγωγή δεν είχαν αναμενόμενες τιμές.
    num=input("Enter number of minimum samples in DBSCAN:")
    distance=input("Enter eps of DBScan:")

    try:
        minsamples=int(num)
        
        distance=float(distance)

        dbscan=DBSCAN(eps=distance,min_samples=minsamples)
        dbscan_clusters=dbscan.fit_predict(X)
        print ("DBSCAN",Counter(dbscan.labels_))

        X["cluster"]=dbscan_clusters
        dbscanscluster_values=sorted(X['cluster'].unique())


        ##Εδώ τυπώνουμε τις ημέρες-outliers. Ο αλγόριθμος DBSCAN που υπάρχει στη python βάζει τα outliers σε ένα "cluster" με τιμή -1.Συνεπώς
        ##αν υπάρχουν outliers, θα υπάρχουν στο cluster -1.

        X["Date"] = X1["Date"]

        outliers=[]
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

        fig = px.scatter(X,x="Sources",y="Demands",hover_name="Date",color="cluster-name",labels={
            "Sources":"Variance of Sources",
            "Demands":"Variance of Demands",
            "cluster":"Clusters"
        },
        title="Sources vs Demands for hours betweeen {}:00-{}:00".format(start_time,end_time)
        )
        fig.show()
        return "GOOD"
    except ValueError:
        print("Wrong Input")
    except KeyboardInterrupt:
        print("Process interrupted")




