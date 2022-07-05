'''
Here we do some unittesting from the functions of the functions.py file of the graphics folder

Requires python's sys,unittest,os libraries
and the code from the file "functions.py" of the module "data_analysis/graphics" of the project folder.

'''

import unittest
import sys 
import os

real_path = os.path.realpath(__file__)##path of current file
dir_path = os.path.dirname(real_path)
root_path = os.path.dirname(dir_path)##root path of project

sys.path.append(root_path)

import data_analysis

from data_analysis.graphics.functions import *

os.chdir(dir_path)

class TestGetTime(unittest.TestCase):
    '''A class that does unittesting of the function chechTime of functions.py'''
    def runTest(self):
        ''' A function that does some examples of unittesting '''
        self.assertEqual(checkTime("10:00"),"10:00","Wrong Input")
        self.assertEqual(checkTime("asdsadsadasd"),None,"Wrong Input")
        self.assertEqual(checkTime("1:00"),None,"Wrong Input")
        self.assertEqual(checkTime("01:00"),"01:00","Wrong Input")
        self.assertEqual(checkTime("10:21"),None,"Wrong Input")
        self.assertEqual(checkTime("10-00"),None,"Wrong Input")
        self.assertEqual(checkTime("ww:00"),None,"Wrong Input")
        self.assertEqual(checkTime("10:ww"),None,"Wrong Input")

class TestFileName(unittest.TestCase):
    '''A class that does unittesting of the function checkFileName of functions.py'''
    def runTest(self):
        ''' A function that does some examples of unittesting'''
        self.assertEqual(checkFileName("20200120"),"2020-01-20","Wrong Input")
        self.assertEqual(checkFileName("20211120"),"2021-11-20","Wrong Input")              
        self.assertEqual(checkFileName("202111200"),None,"Wrong Input")  
        self.assertEqual(checkFileName("2021-11-20"),None,"Wrong Input")
        self.assertEqual(checkFileName("asdfghjk"),None,"Wrong Input")  
        self.assertEqual(checkFileName("12345678"),None,"Wrong Input")

unittest.main()


