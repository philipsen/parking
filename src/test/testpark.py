'''
Created on Mar 11, 2015

@author: wim
'''
import unittest

from config import nummers
from webscrape import webscrape


class Test(unittest.TestCase):


    def test_gethist(self):
        scrape = webscrape.WebScrape("firefox")
        nummer = nummers[0]    
        print "n = ", nummer
        (rem, res) = scrape.get_history(nummer['nr'], nummer['pin'])
        print("rem " + rem)
        self.assertTrue(len(res) > 0, "there is a history")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_gethist']
    unittest.main()
