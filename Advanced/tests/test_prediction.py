'''
Tests `input prediction.py` module. 

Requires `unittest` library to make tests, 
`numpy` library to manipulate data, 
`sys` and `os` libraries to manipulate paths.
'''

import unittest
import numpy as np
import sys 
import os

real_path = os.path.realpath(__file__)
dir_path = os.path.dirname(real_path)
root_path = os.path.dirname(dir_path)

sys.path.append(root_path)

import neural_network
from neural_network.input_prediction import *

os.chdir(dir_path)

class TestPrediction(unittest.TestCase): 
    '''
    Class used to unit test `input_prediction.py` module

    Methods
    -------
    test_input_prediction()
        Tests output of `input_prediction` method on `input_prediction.py` module according to already known prediction output, according to model
    test_subtraction()
        Tests output of subtraction method on `input_prediction.py` module according to already known value
    test_data_type()
        Tests type of data returned by `convert_data_types` method on `input_prediction.py` module according to already known shape
    '''

    demands = [['22216.'],['22106.'],['22130.'],['22040.'],['21963.']]
    demands = np.array(demands)
    renewables = [['6538.'],['6594.'],['6630.'],['6569.'],['6572.']]
    renewables = np.array(renewables)

    difs = []

    def test_input_prediction(self): 
        '''Tests output of `input_prediction` method on `input_prediction.py` module according to already known prediction output, according to model'''

        prediction = input_prediction(self.demands, self.renewables)
        prediction = round(prediction[0], 1)
        
        self.assertEqual(prediction, 15564.0)

    def test_subtraction(self): 
        '''Tests output of `subtraction` method on `input_prediction.py` module according to already known value'''

        self.difs = subtraction(self.demands, self.renewables)
        correctDifs = [15678.,15512.,15500.,15471.,15391.]

        self.assertEqual(self.difs, correctDifs)

    def test_data_type(self): 
        '''Tests type of data returned by `convert_data_types` method on `input_prediction.py` module according to already known shape'''

        differences = convert_data_types(self.difs)

        self.assertEqual(differences.shape, (1, 0, 1))


if __name__ == '__main__': 

    unittest.main()
        