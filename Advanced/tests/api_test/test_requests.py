'''
Tests `RestAPI.py` module. 

Requires `pytest` library to make tests, 
`sys` and `os` libraries to manipulate paths and 
`create_app` method of `RestAPI` module on `neural_network` package. 
'''

import pytest
import os 
import sys 

real_path = os.path.realpath(__file__)
dir_path = os.path.dirname(real_path)
dir_path = os.path.dirname(dir_path)
root_path = os.path.dirname(dir_path)

sys.path.append(root_path)

import neural_network
from neural_network.RestAPI import create_app

os.chdir(dir_path)

def test_response():
    '''Tests response to POST HTTP method on app made by `RestAPI` module'''
    
    app = create_app()
    with app.test_client() as client:  
        response = client.post("/form", data = {
            "demand1" : "0", "renewable1" : "0", 
            "demand2" : "0", "renewable2" : "0", 
            "demand3" : "0", "renewable3" : "0", 
            "demand4" : "0", "renewable4" : "0", 
            "demand5" : "0", "renewable5" : "0", 
        })
        assert response.status_code == 200