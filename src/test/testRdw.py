'''
Created on Mar 7, 2015

@author: wim
'''
try:
    from config import config
except IOError:
    pass

import unittest
from webscrape import webscrape
from database import database

#from nose.tools import nottest

class Test(unittest.TestCase):
    
    def testIllegalKenteken(self):
        try:
            browser = config['browser']
        except(KeyError):
            browser = "firefox"

        web_scrape = webscrape.WebScrape(browser)    
        rdw_info = web_scrape.get_rdw_info("****")
        self.assertEqual(rdw_info["kleur"], "onbekend", "kenteken *** heeft geen info")


    def testGetKenten(self):

        try:
            browser = config['browser']
        except(KeyError):
            browser = "firefox"

        web_scrape = webscrape.WebScrape(browser)
        rdw_info = web_scrape.get_rdw_info("58JRNK")
        
        expect = {'naam': u'TOYOTA COROLLA VERSO', 'InrichtingCodeOmschrijving': u'stationwagen', 'merk': u'TOYOTA', 
                  'kleur': 'Blauw', 'kenteken': '58JRNK'} 
 
        print rdw_info
        print expect
         
        self.assertDictEqual(expect, rdw_info, "Info 1 klopt niet")
        
        # test for with unknown color
        rdw_info = web_scrape.get_rdw_info("6VXR12")
        print 'rdw info = ', rdw_info
        expect = {'naam': u'TRANSIT/TOURNEO', 'merk': u'FORD', 'kleur': 'onbekend', 
                  'InrichtingCodeOmschrijving': u'gesloten opbouw', 'kenteken': "6VXR12"}
        self.assertDictEqual(expect, rdw_info, "Info 2 klopt niet")

    def testKentekenDb(self):
        expect1 = {'naam': u'TOYOTA COROLLA VERSO', 'InrichtingCodeOmschrijving': u'stationwagen',
                   'merk': u'TOYOTA', 'kleur': u'Blauw', 'kenteken': '58JRNK'}
        
        expect2 = {'naam': u'TRANSIT/TOURNEO', 'merk': u'FORD', 'kleur': 'onbekend',
                   'InrichtingCodeOmschrijving': u'gesloten opbouw', 'kenteken': "6VXR12"}   
        
        db2 = database.DataBase()
        db = db2.get_test_db()
        kentekens = db.kentekens
        self.assertEqual(kentekens.count(), 0, "db needs to be empty")
        
        kentekens.insert(expect1)
        kentekens.insert(expect2)
        
        self.assertEqual(kentekens.count(), 2, "db needs 2 entries")

    def testAddKenteken(self):
        expect1 = {u'InrichtingCodeOmschrijving': u'stationwagen', 
                   u'naam': u'TOYOTA COROLLA VERSO', u'kleur': u'Blauw',
                   u'merk': u'TOYOTA', u'kenteken': u'58JRNK'}
        db2 = database.DataBase()
        db = db2.get_test_db()
        kentekens = db.kentekens
        self.assertEqual(kentekens.count(), 0, "db needs to be empty")
        i1 = db2.get_kenteken_info(kentekens, '58JRNK')
        expect1['_id'] = i1['_id']
        print expect1
        print i1
     
        self.assertEqual(kentekens.count(), 1, "db needs have 1")
        self.assertDictEqual(expect1, i1, "Info 1 klopt niet here")    
    
        i2 = db2.get_kenteken_info(kentekens, '58JRNK')
        expect1['_id'] = i2['_id']
        self.assertEqual(kentekens.count(), 1, "db needs to have 1")
        #print(i2)
        self.assertDictEqual(expect1, i2, "Info 2 klopt niet")    
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testRdw']
    unittest.main()
