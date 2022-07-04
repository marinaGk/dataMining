from neural_network.withRelu import * 
import unittest
import numpy as np 

class TestPrediction: 

    def test_input_prediction(self): 

        demands = [['22216.']['22106.']['22130.']['22040.']['21963.']]
        demands = np.array(demands)
        renewables = [['6538.']['6594.']['6630.']['6569.']['6572.']]
        renewables = np.array(renewables)

        #15086.36

        prediction = input_prediction(demands, renewables)
        
