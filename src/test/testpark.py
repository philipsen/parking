'''
Created on Mar 11, 2015

@author: wim
'''
import unittest

from config import nummers
from webscrape import webscrape

from nose.tools import nottest

class Test(unittest.TestCase):

    def test_proc_park_entry(self):
        scrape = webscrape.WebScrape("firefox")
        res2= [u'11-03-2015 13:19\n11-03-2015 15:30\n51LGS9\n2 uur 11 min',
               u'07-03-2015 15:17\n07-03-2015 17:11\n94LVJ7\n1 uur 55 min',
               u'07-03-2015 14:37\n07-03-2015 16:09\n04NNTN\n1 uur 32 min',
               u'07-03-2015 10:01\n07-03-2015 11:01\n14FSRS\n1 uur', 
               u'07-03-2015 09:51\n07-03-2015 09:51\n14FSRS',
            u'06-03-2015 22:33\n06-03-2015 23:58\n14FSRS\n1 uur 25 min', u'04-03-2015 16:54\n04-03-2015 17:24\n63HFLD\n30 min', u'04-03-2015 13:31\n04-03-2015 14:31\n74HST7\n1 uur', u'04-03-2015 10:00\n6VXR12\n30 min', u'']
        for r in res2[0:4]:
            #print r
            proc_item = scrape.proc_item(r, 'naam')
            #print proc_item
            self.assertTrue(proc_item is not None, "item needs top be valid")
            #print proc_item
            self.assertGreater(len(proc_item), 0, "item can not be empty")
        r = res2[4]
        proc_item = scrape.proc_item(r, 'naam')
        self.assertFalse(proc_item is not None, "item is invalid")

    @nottest
    def test_gethist(self):
        scrape = webscrape.WebScrape("firefox")
        nummer = nummers[0]    
        print "n = ", nummer
        (rem, res) = scrape.get_history(nummer['nr'], nummer['pin'])
        print("rem " + rem)
        self.assertTrue(len(res) > 0, "there is a history")

        proc = scrape.proc_item(res[0], nummer['name'])
        print proc
        self.assertTrue(len(proc) > 0, "item is not empty")
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_gethist']
    unittest.main()
