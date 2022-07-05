'''
Used to make prediction for future non-renewable energy requirements using neural network model.

Requires `os` and `sys` library to manipulate paths, 
`pandas` and `numpy` library to format and edit data, 
the `load_module` function from `keras.models` to load given model and 
the `path` module of local `data_analysis` package to determine file path. 

Can be imported as module. 

Contains functions: 

    *subtraction - subtracts renewable energy from demand to find non renewable requirement
    *convert_data_types - 
'''

import os 
import numpy as np
import pandas as pd
from keras.models import load_model
from data_analysis.path import *

def subtraction(demands, renewables): 
    '''
    Used by `input_prediction` of same module to find non-renewable energy requirements given user input. 

    Parameters
    ----------
    demands: list
        Current energy demands according to user input
        More than zero and always exists according to HTML restrictions  
    renewables: list 
        Current renewable energy production according to user input 
        More than zero and always exists according to HTML restrictions

    Returns
    -------
    list 
        A list containing difference of demand and renewable energy for each input -> 
        non-renewable energy required
    '''
    
    difs = []

    for i in range(5): 
        dif = float(demands[i]) - float(renewables[i])
        difs.append(dif) 

    return difs

def convert_data_types(difs): 
    '''
    Used by `input_prediction` of same module to turn lists into appropriate data type to be used for prediction. 

    Parameters
    ----------
    difs: list 
        List of non-renewable energy requirements 

    Returns
    ------- 
    numpy array 
        A numpy array of one row containing initial values as elements of row
    '''

    differences = pd.DataFrame()
    data = []

    differences.insert(0, 'Difference', difs)
    npdf = differences.to_numpy()
    data.append(npdf)
    data = np.array(data)
    print(data)

    return data

def input_prediction(demands, renewables): 
    '''
    Used to make prediction according to input. 

    Parameters
    ----------
    demands: list
        Current energy demands according to user input
        More than zero and always exists according to HTML restrictions 
    renewables: list 
        Current renewable energy production according to user input 
        More than zero and always exists according to HTML restrictions

    Returns
    -------
    element of list
        A list of a single element that is the predicted value of non-renewable energy requirement. 
    '''

    differences = pd.DataFrame()
    difs = subtraction(demands, renewables)
    data = convert_data_types(difs)

    real_path = os.path.realpath(__file__)
    real_path = resolve_path(real_path)
    dir_path = os.path.dirname(real_path)
    os.chdir(dir_path)

    model1 = load_model('model/')

    prediction = model1.predict(data).flatten()

    return prediction