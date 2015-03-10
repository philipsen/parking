'''
Created on Mar 7, 2015

@author: wim
'''
try:
    from config import config
except:
    pass

import unittest
from WebScrape import WebScrape
from DataBase import DataBase
#from DataBase import DataBase

#from nose.tools import nottest

class Test(unittest.TestCase):

    def testGetKenten(self):

        try:
            browser = config['browser']
        except:
            browser = "firefox"

        web_scrape = WebScrape.WebScrape(browser)
        rdw_info = web_scrape.getRdwInfo("58JRNK")
        expect = {'naam': u'TOYOTA COROLLA VERSO', 'InrichtingCodeOmschrijving': u'stationwagen', 
                  'merk': u'TOYOTA', 'kleur': u'Blauw', 'kenteken': '58JRNK'}
        #print(rdw_info)
        self.assertDictEqual(expect, rdw_info, "Info 1 klopt niet")

        rdw_info = web_scrape.getRdwInfo("6VXR12")
        #print(rdw_info)
        expect = {'naam': u'TRANSIT/TOURNEO', 'merk': u'FORD', 'kleur': 'onbekend', 
                  'InrichtingCodeOmschrijving': u'gesloten opbouw', 'kenteken': "6VXR12"}
        self.assertDictEqual(expect, rdw_info, "Info 2 klopt niet")

    def testKentekenDb(self):
        expect1 = {'naam': u'TOYOTA COROLLA VERSO', 'InrichtingCodeOmschrijving': u'stationwagen',
                   'merk': u'TOYOTA', 'kleur': u'Blauw', 'kenteken': '58JRNK'}
        
        expect2 = {'naam': u'TRANSIT/TOURNEO', 'merk': u'FORD', 'kleur': 'onbekend',
                   'InrichtingCodeOmschrijving': u'gesloten opbouw', 'kenteken': "6VXR12"}   
        
        db2 = DataBase.DataBase()
        db = db2.get_test_db()
        kentekens = db.kentekens
        self.assertEqual(kentekens.count(), 0, "db needs to be empty")
        
        kentekens.insert(expect1)
        kentekens.insert(expect2)
        
        self.assertEqual(kentekens.count(), 2, "db needs 2 entries")

    def testAddKenteken(self):
        expect1 = {'naam': u'TOYOTA COROLLA VERSO', 'InrichtingCodeOmschrijving': u'stationwagen',
                   'merk': u'TOYOTA', 'kleur': u'Blauw', 'kenteken': '58JRNK'}
        db2 = DataBase.DataBase()
        db = db2.get_test_db()
        kentekens = db.kentekens
        self.assertEqual(kentekens.count(), 0, "db needs to be empty")
        i1 = db2.get_kenteken_info(kentekens, '58JRNK')
        expect1['_id'] = i1['_id']
        self.assertEqual(kentekens.count(), 1, "db needs have 1")
        self.assertDictEqual(expect1, i1, "Info 1 klopt niet")    
     
        i2 = db2.get_kenteken_info(kentekens, '58JRNK')
        expect1['_id'] = i2['_id']
        self.assertEqual(kentekens.count(), 1, "db needs to have 1")
        #print(i2)
        self.assertDictEqual(expect1, i2, "Info 2 klopt niet")    
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testRdw']
    unittest.main()
