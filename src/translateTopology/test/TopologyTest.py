'''
Created on Mar 1, 2013

@author: nudelg01
'''
import unittest

from translateTopology.translateTopology import *

class TestTop(unittest.TestCase):
    def testTop(self):
        result = str2num('2')
        self.assertEqual(result, 2, "failed")

class TestGvgen(unittest.TestCase):
    def setUp(self):
        self.graph = GvGen('Here is a title hold place')
    
    def tearDown(self):
        self.graph = None

    def testGvGen(self):
        self.assertTrue(isinstance(self.graph, GvGen), "graph isn't an instance of GvGen")

if __name__ == '__main__':
    unittest.main()