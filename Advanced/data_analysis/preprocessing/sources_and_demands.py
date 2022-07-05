'''
Merges all source and demand files into one and creates necessary columns in DataFrame to speed later processes up. 

Requires `pandas` for data manipulation and `os` for path manipulation.
'''

import os
import pandas as pd

def data_merge(): 
    '''Makes file containing both sources and demands records'''

    real_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(real_path)
    dir_path = os.path.dirname(dir_path)
    root_path = os.path.dirname(dir_path)

    data_path = "{}\data".format(root_path)
    os.chdir(data_path) 

    demands_file = data_path + "\\merged_demand_files.csv"
    sources_file = data_path + "\\merged_source_files.csv"

    demands_df = pd.read_csv(demands_file)
    sources_df = pd.read_csv(sources_file)

    cols = ['Day ahead forecast', 'Hour ahead forecast', 'Current demand']
    for i in cols: 
        column = demands_df[i].tolist()
        sources_df[i] = column

    new_path = data_path + "\\merged_files.csv"
    sources_df.info()
    sources_df.to_csv(new_path, index=False)

