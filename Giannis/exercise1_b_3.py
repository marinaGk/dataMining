import pandas as pd
from os import X_OK, listdir
from os.path import isfile, join
import os
import random
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
import numpy as np
from sklearn.datasets import make_friedman1
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import silhouette_score
from collections import Counter
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import MiniBatchKMeans
from sklearn.cluster import SpectralClustering
from sklearn.cluster import Birch
from math import sqrt
import plotly.express as px


directory=os.getcwd()

##Προεπεξεργασία των Δεδομένων. Εδώ επεξεργαζόμαστε τα δεδομένα μας ώστε σε κάθε αρχείο excel που βρίσκεται στους φακέλους sources και demands που μας δίνονται
##να έχει τον ίδιο αριθμό δεδομενών (288). Σε περίπτωση που ένα αρχείο έχει παραπάνω δεδομένα, τα διαγράφουμε. Αν σε ένα αρχείο λείπουν δεδομένα, φροντίζουμε ώστε
##ώστε να μην χαλάει η ροή των δεδομένων, βάζοντας ως τιμές σε αυτά τις τιμές του προηγούμενου στιγμιοτύπου. Μέρες που δεν έχουν δεδομένα δεν τις λαμβάνουμε υπόψη(πχ 2019-02-28).
##Τέλος, αφού κάνουμε την προεπεξεργασία, φτιάχνουμε νέους φακέλους processed_sources και processed_demands στους οποίους και βάζουμε τα επεξεργασμένα αρχεία των sources και demands
##αντίστοιχα που φτιάξαμε.

##print("SOURCES")
##mypath="{}/sources".format(directory)
##os.chdir(mypath)
##
##df=pd.read_csv("20190101.csv")
##time=df["Time"]
##
##sourcesfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
##
##sources_headers = ["Time","Solar","Wind","Geothermal","Biomass","Biogas","Small hydro","Coal","Nuclear","Natural gas","Large hydro","Batteries","Imports","Other"]
##
##for x in range(len(sourcesfiles)):
##    try:
##        mypath="{}/sources".format(directory)
##        os.chdir(mypath)
##        list_tuples = []
##        df1 = pd.read_csv(sourcesfiles[x])
##        print(sourcesfiles[x][0:8])
##        for j in range(len(df1)):
##            if j==len(time):
##                continue
##            d=[]
##            d.append(time[j])
##            for z in range(1,len(sources_headers)):
##                if np.isnan(df1.iloc[j,z])==True:
##                    if np.isnan(df1.iloc[0,z])==True:
##                        d.append(0)
##                    else:
##                        d.append(list_tuples[-1][z])
##                else:
##                    d.append(df1.iloc[j,z])
##            list_tuples.append(d)
##        if len(time)>len(df1):
##            print(len(time)-len(df1))
##            for l in range(len(time)-len(df1)):
##                d=[]
##                d.append(time[len(df1)+l])
##                print(l,x,time[len(df1)+l])
##                for z in range(1,len(sources_headers)):
##                    d.append(list_tuples[-1][z])
##                list_tuples.append(d)
##        mypath="{}/processed_sources".format(directory)
##        os.chdir(mypath)
##        new_csv = pd.DataFrame(list_tuples)
##        new_csv.columns = sources_headers
##        new_csv.to_csv( "new_{}.csv".format(sourcesfiles[x][0:8]), index=False, encoding='utf-8-sig')
##    except:
##        continue
##
##print("DEMANDS")
##mypath="{}/demand".format(directory)
##os.chdir(mypath)
##
##demandfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
##
##demands_headers = ["Time","Day ahead forecast","Hour ahead forecast","Current demand"]
##
##for x in range(len(demandfiles)):
##    try:
##        mypath="{}/demand".format(directory)
##        os.chdir(mypath)
##        list_tuples = []
##        df1 = pd.read_csv(demandfiles[x])
##        print(demandfiles[x][0:8])
##        for j in range(len(df1)):
##            if j==len(time):
##                continue
##            d=[]
##            d.append(time[j])
##            for z in range(1,len(demands_headers)):
##                if np.isnan(df1.iloc[j,z])==True:
##                    if np.isnan(df1.iloc[0,z])==True:
##                        d.append(0)
##                    else:
##                        d.append(list_tuples[-1][z])
##                else:
##                    d.append(df1.iloc[j,z])
##            list_tuples.append(d)
##        if len(time)>len(df1):
##            print(len(time)-len(df1))
##            for l in range(len(time)-len(df1)):
##                d=[]
##                d.append(time[len(df1)+l])
##                print(l,x,time[len(df1)+l])
##                for z in range(1,len(demands_headers)):
##                    d.append(list_tuples[-1][z])
##                list_tuples.append(d)
##        mypath="{}/processed_demands".format(directory)
##        os.chdir(mypath)
##        new_csv = pd.DataFrame(list_tuples)
##        new_csv.columns = demands_headers
##        new_csv.to_csv( "new_{}.csv".format(demandfiles[x][0:8]), index=False, encoding='utf-8-sig')
##    except:
##        continue


##Για τα επεξεργασμένα αρχεία των φακέλων processed_sources και processed_demands βρίσκουμε για κάθε χρονκή στιγμή της ημέρας το άθροισμα
##της ενέργειας και επιπλέον βρίσκουμε για κάθε ημέρα στατιστικά στοιχεία όπως η μέση τιμή,η διακύμανση και η τυπική απόκλιση.


# mypath="{}/processed_sources".format(directory)
# os.chdir(mypath)

# files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
# dates = [f[4:12] for f in listdir(mypath) if isfile(join(mypath, f))]
# sources_headers = ["Time","Solar","Wind","Geothermal","Biomass","Biogas","Small hydro","Coal","Nuclear","Natural gas","Large hydro","Batteries","Imports","Other"]

# demands_headers = ["Time","Day ahead forecast","Hour ahead forecast","Current demand"]

# stats_of_day_sources=[]
# stats_of_day_demands=[]

# sources_of_days=[]
# demands_of_days=[]

# sources_of_day=[]
# demands_of_day=[]

# df0 = pd.read_csv(files[0])
# times = df0["Time"]
# time = len(df0)

# ## Μεταβλητές που ορίζουν τις ώρες από τις οποίες παίρνουμε τα δεδομένα. Βάζοντας k=0 και l=4, παίρνουμε δεδομένα των ημερών καθόλη τη διάρκεια της ημέρας,ενώ για k=0 και l=1, 
# ## παίρνουμε δεδομένα για τις ώρες 00:00 - 06:00,για k=1,l=2 παίρνουμε δεδομένα για τις ώρες 06:00 - 12:00,για k=2 και l=3 παίρνουμε δεδομένα για τις ώρες 12:00 - 18:00, για 
# ## k=3 και l=4 παίρνουμε δεδομένα για τις ώρες 18:00 - 24:00
# k=3
# l=4
# print(int(k*288/4),int(l*288/4))
# for i in range(len(files)):
#     print(files[i][4:12])
#     sources_of_day=[]
#     demands_of_day=[]
#     mypath="{}/processed_sources".format(directory)
#     os.chdir(mypath)
#     df1 = pd.read_csv(files[i])
#     for j in range(int(k*len(df1)/4),int(l*len(df1)/4)):
#         total=0
#         for x in range(1,len(sources_headers)):
#             total+=df1.iloc[j,x]
#         sources_of_day.append(total) 
#         # print("Sources",total)

#     mypath="{}/processed_demands".format(directory)
#     os.chdir(mypath)
#     df2 = pd.read_csv(files[i])
#     for j in range(int(k*len(df2)/4),int(l*len(df2)/4)):
#         total1=0
#         for x in range(1,len(demands_headers)):
#             total1+=df2.iloc[j,x]
#         demands_of_day.append(total1)
#         # print("Demands",total1)

#     sources_of_day = np.array(sources_of_day)
#     demands_of_day = np.array(demands_of_day)

#     sources_mean = np.mean(sources_of_day)
#     demands_mean = np.mean(demands_of_day)     

#     sources_var = np.var(sources_of_day)
#     demands_var = np.var(demands_of_day)     

#     sources_std = np.std(sources_of_day)
#     demands_std = np.std(demands_of_day)     

#     stats_of_day_sources.append([sources_mean,sources_var,sources_std])
#     stats_of_day_demands.append([demands_mean,demands_var,demands_std])

# ##Στην συνέχεια, αφού κάνουμε scale τα δεδομένα, δημιουργούμε ένα DataFrame όπου κάθε ημέρα χαρακτηρίζεται από την διακύμανση της ενέργειας που υπάρχει 
# ##στα sources και τη διακύμανση της ενέργειας που υπάρχει στα demands και το αποθηκεύουμε σε ένα csv αρχείο. Έχουν φτιαχτεί ήδη 4 αρχεία csv
# ##Το Variance.csv που έχει δεδομένα για όλες τις ώρες της ημέρας
# ##Το Variance-0.csv που έχει δεδομένα για τις ώρες 00:00-06:00
####Το Variance-1.csv που έχει δεδομένα για τις ώρες 06:00-12:00
####Το Variance-2.csv που έχει δεδομένα για τις ώρες 12:00-18:00
####Το Variance-3.csv που έχει δεδομένα για τις ώρες 18:00-24:00


# scaler = StandardScaler()
# L=[]
# L1=[]
# for i in range(len(stats_of_day_sources)):
#     L.append([files[i][4:12],stats_of_day_sources[i][1],stats_of_day_demands[i][1]])
#     L1.append([stats_of_day_sources[i][1],stats_of_day_demands[i][1]])

# L2 = scaler.fit_transform(L1)

# L3=[]
# for i in range(len(L)):
#     date=L[i][0]
#     year=date[0:4]
#     month = date[4:6]
#     day = date[6:8]
#     date = year + "-" + month + "-" + day
#     L3.append([date,L2[i][0],L2[i][1]])



# X =  pd.DataFrame(L2,columns=["Sources","Demands"])
# X1 = pd.DataFrame(L3,columns=["Date","Sources","Demands"])

# mypath="{}".format(directory)
# os.chdir(mypath)
# new_csv = pd.DataFrame(X1)
# new_csv.to_csv( "Variance-3.csv", index=False, encoding='utf-8-sig')

##Αφού φορτώσουμε τα δεδομένα από το επιθυμητό αρχείο, μπορούμε να αναπαραστήσουμε τα δεδομένα σε μια γραφική παράσταση Sources vs Demands 

mypath="{}".format(directory)
os.chdir(mypath)
X = pd.read_csv("Variance.csv")
X1 = []
for i in range(len(X)):
    X1.append([X["Sources"][i],X["Demands"][i]])
X1=pd.DataFrame(X1,columns=["Sources","Demands"])
colormap=['b','g','r','c','m','y','k','slateblue','springgreen','indigo','teal','lightcoral','gold']

fig = px.scatter(X,x="Sources",y="Demands",hover_name="Date",labels={
    "Sources":"Variance of Sources",
    "Demands":"Variance of Demands"
},
title="Sources vs Demands"
)
fig.show()


##Ένας αποδοτικός αλγόριθμος για την έυρεση των outliers είναι ο DBSCAN. Βάζοντας κατάλληλες παραμέτρους min_samples και eps, μπορούμε να βρούμε
##τις ημέρες εκείνες που η ζήτηση ή η παραγωγή δεν είχαν αναμενόμενες τιμές.
try:  
    num=input("Enter number of minimum samples in DBSCAN:")
    minsamples=int(num)

    # neighbors=NearestNeighbors(n_neighbors=2)
    # neighbors_fit=neighbors.fit(X)
    # distances,indices=neighbors_fit.kneighbors(X)
    # distances=np.sort(distances,axis=0)
    # distances=distances[:,1]
    # plt.plot(distances)
    # plt.show()


    distance=input("Enter eps of DBScan:")
    distance=float(distance)

    dbscan=DBSCAN(eps=distance,min_samples=minsamples)
    dbscan_clusters=dbscan.fit_predict(X1)
    print ("DBSCAN",Counter(dbscan.labels_))

    X["cluster"]=dbscan_clusters
    print(X)
    dbscanscluster_values=sorted(X['cluster'].unique())


    ##Εδώ τυπώνουμε τις ημέρες-outliers. Ο αλγόριθμος DBSCAN που υπάρχει στη python βάζει τα outliers σε ένα "cluster" με τιμή -1.Συνεπώς
    ##αν υπάρχουν outliers, θα υπάρχουν στο cluster -1.

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
    title="Search for outliers Sources vs Demands for hours betweeen 18:00-24:00"
    )
    fig.show()
except ValueError:
    print("Wrong Input")
except KeyboardInterrupt:
    print("Process interrupted")








