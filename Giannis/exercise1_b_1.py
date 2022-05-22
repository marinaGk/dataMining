import pandas as pd
from os import listdir
from os.path import isfile, join
import os
import random
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import silhouette_score
from collections import Counter
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import MiniBatchKMeans


directory=os.getcwd()

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

##mypath="{}/processed_sources".format(directory)
##os.chdir(mypath)
##
##files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
##
##sources_headers = ["Time","Solar","Wind","Geothermal","Biomass","Biogas","Small hydro","Coal","Nuclear","Natural gas","Large hydro","Batteries","Imports","Other"]
##
##demands_headers = ["Time","Day ahead forecast","Hour ahead forecast","Current demand"]
##
##
##wholedata = []
##for i in range(len(files)):
##    day = files[i][4:12]
##    print(day)
##
##
##    mypath="{}/processed_sources".format(directory)
##    os.chdir(mypath)
##    df1 = pd.read_csv(files[i])
##
##    mypath="{}/processed_demands".format(directory)
##    os.chdir(mypath)
##    df2 = pd.read_csv(files[i])
##    
##    for x in range(len(df1)):
##        d=[]
##        d.append(day)
##        d.append(df1["Time"][x])
##        for y in range(1,len(sources_headers)):
##            d.append(df1.iloc[x,y])
##        for y in range(1,len(demands_headers)):
##            d.append(df2.iloc[x,y])         
##        wholedata.append(d)
##
##headers=["Day","Time","Solar","Wind","Geothermal","Biomass","Biogas","Small hydro","Coal","Nuclear","Natural gas","Large hydro","Batteries","Imports","Other","Day ahead forecast","Hour ahead forecast","Current demand"]
##new_csv = pd.DataFrame(wholedata)
##new_csv.columns = headers
##
##    
##mypath="{}".format(directory)
##os.chdir(mypath)
##new_csv.to_csv( "wholedata1.csv", index=False, encoding='utf-8-sig')
##


######## This function is used in order to find days-outliers for each category of demand or source(energy_type). 
def find_outliers(energy_type):
    ####From the csv flie, we isolate the columns of Date, Time and category of our choice
    df_pivot=df[["Day","Time","{}".format(energy_type)]]
    df_pivot_new=df_pivot.pivot(index="Day",columns="Time")
    print(df_pivot_new)
    scaler=StandardScaler()
##    scaler = MinMaxScaler()
    #### We scale the Data of the category so that its easier for us to find the days-outliers
##    scaler=RobustScaler()
    X=pd.DataFrame(scaler.fit_transform(df_pivot_new["{}".format(energy_type)]),columns=df_pivot_new.columns)
    X=X["{}".format(energy_type)]
    print(X)
    #####Using the sklearn.decomposition library and the PCA method, we reduct the dimensions of our data into 2 dimensions
    ##### in order to have a better visualization of the results.
    pca = PCA(n_components=2)
    reduced_X=pd.DataFrame(pca.fit_transform(X),columns=["X","Y"])
    x=reduced_X["X"]
    y=reduced_X["Y"]
    plt.scatter(x,y)
    plt.show()

    
    K=[i for i in range(2,20)]

    
    ####In order to split the data into clusters with Kmeans,we have to determine the number of clusters.
    ####Below we use two methods , the Elbow Method and the Silhouette analysis 

    
    #ELBOW CURVE
    
    ####First, we calculate the sum of squared distances of all the samples from their closest cluster center(inertia)
    #### We experiment here with a range of cluster numbers from 2 to 20. Then we plot the values
    #### of the inertia for every number of clusters. To determine the optimal number of clusters, we have to
    #### to select the number of clusters at the "elbow", the point in which the inertia starts descreasing
    #### in a linear fashion.

    sum_of_squared_distances=[]
    for k in K:
        try:
            kmeans=KMeans(n_clusters=k)
            kmeans.fit(X)
            sum_of_squared_distances.append(kmeans.inertia_)
        except:
            continue
    
    plt.plot(K,sum_of_squared_distances,'bx-')
    plt.xlabel('Values of k')
    plt.ylabel('Sum of squared distances/Inertia')
    plt.title('Elbow method for optimal k')
    plt.show()
    
    #Silhouette analysis
    
    ####Silhouette value is a measure of how similar a point is to its own cluster compared
    ####to other clusters. It ranges from -1 to 1, where a high value indeicates that a point has a good match
    ####with the cluster it belongs. We take the average of the silhoutte across all load-profiles in order to have a global view of how the
    ####algorithm is perfoming. Here we experment with a range of cluster number (from 2 to 20). Here we create a silhouette score vs number of clusters graph.
    ####We pick the number of clusters after the one that maximizes the silhouette score.

    silhouette_avg=[]
    for k in K:
        try:
            kmeans=KMeans(n_clusters=k)
            kmeans.fit(X)
            cluster_labels=kmeans.labels_
            silhouette_avg.append(silhouette_score(X,cluster_labels))
        except:
            continue

    plt.plot(K,silhouette_avg,'bx-')
    plt.xlabel('Values of k')
    plt.ylabel('Silhoutte Score')
    plt.title('Silhouette analysis For Optimal k')
    plt.show()    



    colormap=['b','g','r','c','m','y','k','slateblue','springgreen','indigo','teal','lightcoral','gold']


    ####User puts the number of clusters
    num=input("Enter number of clusters in KMeans:")
    numclusters=int(num)


    ##KMEANS Algorithm implementation and visualization
    kmeans=KMeans(n_clusters=numclusters)
    kmeans.fit(X)
    centers=kmeans.cluster_centers_
    kmeans_clusters=kmeans.predict(X)
    print("KMEANS",Counter(kmeans.labels_))

    reduced_X["cluster"]=kmeans_clusters
    kmeanscluster_values=sorted(reduced_X["cluster"].unique())
    reduced_centers=pd.DataFrame(pca.transform(centers),columns=["X","Y"])
    for i in kmeanscluster_values:
        x=reduced_X[reduced_X["cluster"]==i]["X"]
        y=reduced_X[reduced_X["cluster"]==i]["Y"]
        plt.scatter(x,y,color=colormap[i])
    plt.scatter(reduced_centers["X"],reduced_centers["Y"],color="black",marker='x',s=300)
    plt.title("KMEANS")
    plt.show()

    ####Here we show the days-outliers for our category( if they exist of course  ). A way of determining
    ####whether a day has values that are not expected, is to see if the cluster that is in, has more or less than
    ####15 points in it.If a cluster has less than 10 points, then we consider all the points-days as outliers.

    num_clusters=[]
    for j in range(len(kmeanscluster_values)):
        num=0
        L=[]
        for i in range(len(reduced_X)):
            if reduced_X["cluster"][i]==kmeanscluster_values[j]:
                L.append(date[i])
                num+=1
        num_clusters.append([num,L])

    outliers=[]
    for i in range(len(num_clusters)):
        if num_clusters[i][0]<15:
            for j in num_clusters[i][1]:
                outliers.append(j)
    s=" "
    if len(outliers)>0:
        days=' '.join([str(elem) for elem in outliers])
        print("KMeans: Outliers for {} : {}".format(energy_type,days))
    else:
        print("KMeans: No outliers")
    
    ###Here we about to use the DBSCAN algorithm, but he have to determine the number of minimum samples and the
    ###eps factor. The eps factor is a value in which two points are considered neighbors if the distance
    ###between the two points is below the theshold epsilon. Minimum samples determines the minimum number
    ###of neighbors a given point should have in order to be classified as a core point. Here the user sets the number of minimum samples(analog to data).
    ###In order to determine the eps factor we calculate for each point, the distance to the nearest n points(n_neighbors)
    ###using the NearestNeighbors method. The kneighbors method returns the distances for the closest n_neighbors and the index
    ###for each of those points.We sort the distances and we plot the results. The optimal value for epsilon
    ### will be found at the point of maximum curvature.

    num=input("Enter number of minimum samples in DBSCAN:")
    minsamples=int(num)
    neighbors=NearestNeighbors(n_neighbors=2)
    neighbors_fit=neighbors.fit(X)
    distances,indices=neighbors_fit.kneighbors(X)
    distances=np.sort(distances,axis=0)
    distances=distances[:,1]
    plt.plot(distances)
    plt.show()

    
    distance=input("Enter eps of DBScan:")
    distance=float(distance)

    ##DBSCAN Algorithm implementation and visualization
    dbscan=DBSCAN(eps=distance,min_samples=minsamples)
    dbscan_clusters=dbscan.fit_predict(X)
    print ("DBSCAN",Counter(dbscan.labels_))
    
    
    reduced_X["cluster"]=dbscan_clusters
    dbscanscluster_values=sorted(reduced_X['cluster'].unique())
    for i in dbscanscluster_values:
        x=reduced_X[reduced_X["cluster"]==i]["X"]
        y=reduced_X[reduced_X["cluster"]==i]["Y"]
        plt.scatter(x,y,color=colormap[i])
        plt.title("DBSCAN")
    plt.show()

    ####Here we show the days-outliers for our category( if they exist of course  ). A way of determining
    ####whether a day has values that are not expected, is to see if the cluster that is in, has more or less than
    ####15 points in it.If a cluster has less than 10 points, then we consider all the points-days as outliers.
    num_clusters=[]
    for j in range(len(dbscanscluster_values)):
        num=0
        L=[]
        for i in range(len(reduced_X)):
            if reduced_X["cluster"][i]==dbscanscluster_values[j]:
                L.append(date[i])
                num+=1
        num_clusters.append([num,L])

    outliers=[]
    for i in range(len(num_clusters)):
        if num_clusters[i][0]<15:
            for j in num_clusters[i][1]:
                outliers.append(j)
    s=" "
    if len(outliers)>0:
        days=' '.join([str(elem) for elem in outliers])
        print("DBSCAN: Outliers for {} : {}".format(energy_type,days))
    else:
        print("DBSCAN: No outliers")
    


    ##Agglomerative Clustering Algorithm implementation and visualization
    model=AgglomerativeClustering(n_clusters=numclusters,affinity="euclidean")
    model.fit(X)
    ac_clusters=model.labels_
    print ("Agglomerative",Counter(model.labels_))
    reduced_X["cluster"]=ac_clusters
    accluster_values=sorted(reduced_X["cluster"].unique())
    for i in accluster_values:
        x=reduced_X[reduced_X["cluster"]==i]["X"]
        y=reduced_X[reduced_X["cluster"]==i]["Y"]
        plt.scatter(x,y,color=colormap[i])
    plt.title("Agglomerative")
    plt.show()
    
    ####Here we show the days-outliers for our category( if they exist of course  ). A way of determining
    ####whether a day has values that are not expected, is to see if the cluster that is in, has more or less than
    ####15 points in it.If a cluster has less than 10 points, then we consider all the points-days as outliers.
    num_clusters=[]
    for j in range(len(dbscanscluster_values)):
        num=0
        L=[]
        for i in range(len(reduced_X)):
            if reduced_X["cluster"][i]==dbscanscluster_values[j]:
                L.append(date[i])
                num+=1
        num_clusters.append([num,L])

    outliers=[]
    for i in range(len(num_clusters)):
        if num_clusters[i][0]<15:
            for j in num_clusters[i][1]:
                outliers.append(j)
    s=" "
    if len(outliers)>0:
        days=' '.join([str(elem) for elem in outliers])
        print("Aglomerative Clustering: Outliers for {} : {}".format(energy_type,days))
    else:
        print("Aglomerative: No outliers")



    ##MinBatchKMeans Clustering Algorithm implementation and visualization
    model=MiniBatchKMeans(n_clusters=numclusters,random_state=0,batch_size=100)
    model.fit(X)
    mbk_clusters=model.labels_
    print ("Agglomerative",Counter(model.labels_))
    reduced_X["cluster"]=mbk_clusters
    mbkcluster_values=sorted(reduced_X["cluster"].unique())
    for i in mbkcluster_values:
        x=reduced_X[reduced_X["cluster"]==i]["X"]
        y=reduced_X[reduced_X["cluster"]==i]["Y"]
        plt.scatter(x,y,color=colormap[i])
    plt.title("MiniBatchKMeans")
    plt.show()


    ####Here we show the days-outliers for our category( if they exist of course  ). A way of determining
    ####whether a day has values that are not expected, is to see if the cluster that is in, has more or less than
    ####15 points in it.If a cluster has less than 10 points, then we consider all the points-days as outliers.
    num_clusters=[]
    for j in range(len(dbscanscluster_values)):
        num=0
        L=[]
        for i in range(len(reduced_X)):
            if reduced_X["cluster"][i]==dbscanscluster_values[j]:
                L.append(date[i])
                num+=1
        num_clusters.append([num,L])

    outliers=[]
    for i in range(len(num_clusters)):
        if num_clusters[i][0]<15:
            for j in num_clusters[i][1]:
                outliers.append(j)
    s=" "
    if len(outliers)>0:
        days=' '.join([str(elem) for elem in outliers])
        print("MinBatchKmeans Clustering: Outliers for {} : {}".format(energy_type,days))
    else:
        print("MinBatchKmeans: No outliers")



if __name__=="__main__":
    df=pd.read_csv("wholedata1.csv")###Loading of our data
    headers=df.columns
    date=df["Day"].unique()
    time=df["Time"].unique()
    L=["Solar","Wind","Geothermal","Biomass","Biogas","Small hydro","Coal","Nuclear","Natural gas","Large hydro","Batteries","Imports","Other","Day ahead forecast","Hour ahead forecast","Current demand"]
    energy=input("Enter the energy type:")###User inputs the type of demand or source in which we find the days-outliers
    while(energy!="."):
        if energy not in L:
            print("Oops. Try again")
        else:
            find_outliers(energy)
        energy=input("Enter the energy type:")


    

