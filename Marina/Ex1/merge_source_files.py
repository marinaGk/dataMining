import pandas as pd 
import os

def merge_sources(): 
    '''Merges all source files into one, required to make data processing faster'''

    real_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(real_path)
    dir_path = dir_path + "\sources\\"
    os.chdir(dir_path) #works inside data directory (sources)

    filelist = []
    row_count = 0 
    days = []
    months = []
    years = []

    df = pd.DataFrame() #dataFrame to be used to store data 
    day_df = pd.DataFrame()

    time_df = pd.read_csv(dir_path + "20190101.csv") #reads sample times from one of the files 
    time = time_df['Time'].tolist()

    for filename in os.listdir(dir_path):

        file = dir_path + filename

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
    
    new_path = os.path.dirname(real_path) + "\\merged_source_files.csv"
    df.info()
    df.to_csv(new_path, index=False)

merge_sources()