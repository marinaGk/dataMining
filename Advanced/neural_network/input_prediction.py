import os 
import numpy as np
import pandas as pd
from keras.models import load_model

def subtraction(demands, renewables): 
    
    difs = []

    for i in range(5): 
        dif = float(demands[i]) - float(renewables[i])
        difs.append(dif) 

    return difs

def convert_data_types(difs): 

    differences = pd.DataFrame()
    data = []

    differences.insert(0, 'Difference', difs)
    npdf = differences.to_numpy()
    data.append(npdf)
    data = np.array(data)
    print(data.shape)
    return data

def input_prediction(demands, renewables): 

    differences = pd.DataFrame()
    difs = subtraction(demands, renewables)
    data = convert_data_types(difs)

    real_path = os.path.realpath(__file__)
    dir_path = os.path.dirname(real_path)
    os.chdir(dir_path)

    model1 = load_model('model/')

    prediction = model1.predict(data).flatten()

    return prediction