import unittest
import numpy as np
import sys 
import os

real_path = os.path.realpath(__file__)
dir_path = os.path.dirname(real_path)
root_path = os.path.dirname(dir_path)

sys.path.insert(0, root_path)
from neural_network.withRelu import input_prediction 

class TestPrediction(unittest.TestCase): 

    def test_input_prediction(self): 

        demands = [['22216.'],['22106.'],['22130.'],['22040.'],['21963.']]
        demands = np.array(demands)
        renewables = [['6538.'],['6594.'],['6630.'],['6569.'],['6572.']]
        renewables = np.array(renewables)

        #15086.37

        prediction = input_prediction(demands, renewables)
        prediction = round(prediction, 2)

        self.assertEqual(prediction, 15086.37)
