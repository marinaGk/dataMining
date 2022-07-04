import unittest

from functions import *
from day_data import *

###Some unittesting 

class TestGetTime(unittest.TestCase):
    def runTest(self):
        self.assertEqual(checkTime("10:00"),"10:00","Wrong Input")
        self.assertEqual(checkTime("asdsadsadasd"),None,"Wrong Input")
        self.assertEqual(checkTime("1:00"),None,"Wrong Input")
        self.assertEqual(checkTime("01:00"),"01:00","Wrong Input")
        self.assertEqual(checkTime("10:21"),None,"Wrong Input")
        self.assertEqual(checkTime("10-00"),None,"Wrong Input")
        self.assertEqual(checkTime("ww:00"),None,"Wrong Input")
        self.assertEqual(checkTime("10:ww"),None,"Wrong Input")
        
class TestGetDate(unittest.TestCase):
    def runTest(self):
        self.assertEqual(checkDate("2020-01-20"),"2020-01-20","Wrong Input")
        self.assertEqual(checkDate("20200120"),None,"Wrong Input")
        self.assertEqual(checkDate("asdsadsadasd"),None,"Wrong Input")
        self.assertEqual(checkDate("2020-01-32"),None,"Wrong Input")
        self.assertEqual(checkDate("2020-02-30"),None,"Wrong Input")
        self.assertEqual(checkDate("wwww-01-32"),None,"Wrong Input")
        self.assertEqual(checkDate("2020-ww-32"),None,"Wrong Input")
        self.assertEqual(checkDate("2020-01-ww"),None,"Wrong Input")
        self.assertEqual(checkDate("2020-01-220"),None,"Wrong Input")
        self.assertEqual(checkDate("2022:04:20"),None,"Wrong Input")
        self.assertEqual(checkDate("2022-12-31"),"2022-12-31","Wrong Input")

class TestFileName(unittest.TestCase):
    def runTest(self):
        self.assertEqual(checkFileName("20200120"),"2020-01-20","Wrong Input")
        self.assertEqual(checkFileName("20211120"),"2021-11-20","Wrong Input")              
        self.assertEqual(checkFileName("202111200"),None,"Wrong Input")  
        self.assertEqual(checkFileName("2021-11-20"),None,"Wrong Input")
        self.assertEqual(checkFileName("asdfghjk"),None,"Wrong Input")  
        self.assertEqual(checkFileName("12345678"),None,"Wrong Input")


unittest.main()


