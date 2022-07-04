import pandas as pd
from os import X_OK, listdir
from os.path import isfile, join
import os
import random
import numpy as np


directory=os.getcwd()

##Προεπεξεργασία των Δεδομένων. Εδώ επεξεργαζόμαστε τα δεδομένα μας ώστε σε κάθε αρχείο excel που βρίσκεται στους φακέλους sources και demands που μας δίνονται
##να έχει τον ίδιο αριθμό δεδομενών (288). Σε περίπτωση που ένα αρχείο έχει παραπάνω δεδομένα, τα διαγράφουμε. Αν σε ένα αρχείο λείπουν δεδομένα, φροντίζουμε ώστε
##ώστε να μην χαλάει η ροή των δεδομένων, βάζοντας ως τιμές σε αυτά τις τιμές του προηγούμενου στιγμιοτύπου. Μέρες που δεν έχουν δεδομένα δεν τις λαμβάνουμε υπόψη(πχ 2019-02-28).
##Τέλος, αφού κάνουμε την προεπεξεργασία, φτιάχνουμε νέους φακέλους processed_sources και processed_demands στους οποίους και βάζουμε τα επεξεργασμένα αρχεία των sources και demands
##αντίστοιχα που φτιάξαμε.Τα αρχεία αυτά υπάρχουν έτοιμα στο data.zip. 

print("SOURCES")
mypath="{}/data/sources".format(directory)
os.chdir(mypath)

df=pd.read_csv("20190101.csv")
time=df["Time"]

sourcesfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

sources_headers = ["Time","Solar","Wind","Geothermal","Biomass","Biogas","Small hydro","Coal","Nuclear","Natural gas","Large hydro","Batteries","Imports","Other"]


for x in range(len(sourcesfiles)):
   try:
       mypath="{}/data/sources".format(directory)
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
       mypath="{}/data/processed_sources".format(directory)
       os.chdir(mypath) 
       new_csv = pd.DataFrame(list_tuples)
       new_csv.columns = sources_headers
       new_csv.to_csv("new_{}.csv".format(sourcesfiles[x][0:8]), index=False, encoding='utf-8-sig')
   except:
       continue

print("DEMANDS")
mypath="{}/data/demand".format(directory)
os.chdir(mypath)

demandfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

demands_headers = ["Time","Day ahead forecast","Hour ahead forecast","Current demand"]

for x in range(len(demandfiles)):
   try:
       mypath="{}/data/demand".format(directory)
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
       mypath="{}/data/processed_demands".format(directory)
       os.chdir(mypath)
       new_csv = pd.DataFrame(list_tuples)
       new_csv.columns = demands_headers
       new_csv.to_csv( "new_{}.csv".format(demandfiles[x][0:8]), index=False, encoding='utf-8-sig')
   except:
       continue

