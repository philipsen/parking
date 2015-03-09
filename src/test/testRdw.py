'''
Created on Mar 7, 2015

@author: wim
'''
import unittest
from WebScrape import WebScrape
from DataBase import DataBase

class Test(unittest.TestCase):

    def testGetKenten(self):
        print("here")
        web_scrape = WebScrape.WebScrape()
        rdw_info = web_scrape.getRdwInfo("58JRNK")
        expect = {'naam': u'TOYOTA COROLLA VERSO', 'InrichtingCodeOmschrijving': u'stationwagen', 
                  'merk': u'TOYOTA', 'kleur': u'Blauw', 'kenteken': '58JRNK'}
        print(rdw_info)
        self.assertDictEqual(expect, rdw_info, "Info 1 klopt niet")

        rdw_info = web_scrape.getRdwInfo("6VXR12", True)
        print(rdw_info)
        expect = {'naam': u'TRANSIT/TOURNEO', 'merk': u'FORD', 'kleur': 'onbekend', 
                  'InrichtingCodeOmschrijving': u'gesloten opbouw', 'kenteken': "6VXR12"}
        self.assertDictEqual(expect, rdw_info, "Info 2 klopt niet")

    def testKentekenDb(self):
        expect1 = {'naam': u'TOYOTA COROLLA VERSO', 'InrichtingCodeOmschrijving': u'stationwagen', 
                  'merk': u'TOYOTA', 'kleur': u'Blauw', 'kenteken': '58JRNK'}
        
        expect2 = {'naam': u'TRANSIT/TOURNEO', 'merk': u'FORD', 'kleur': 'onbekend', 
                  'InrichtingCodeOmschrijving': u'gesloten opbouw', 'kenteken': "6VXR12"}   
        
        db2 = DataBase.DataBase()
        db = db2.getTestDb()
        kentekens = db.kentekens
        self.assertEqual(kentekens.count(), 0, "db needs to be empty")
        
        kentekens.insert(expect1)
        kentekens.insert(expect2)
        
        self.assertEqual(kentekens.count(), 2, "db needs 2 entries")

    def testAddKenteken(self):
        print("\n\n\ntestAddKenteken")

        expect1 = {'naam': u'TOYOTA COROLLA VERSO', 'InrichtingCodeOmschrijving': u'stationwagen', 
                  'merk': u'TOYOTA', 'kleur': u'Blauw', 'kenteken': '58JRNK'}
        print("here")
        db2 = DataBase.DataBase()
        print("here")
        db = db2.getTestDb()
        print("here")
        kentekens = db.kentekens
        print("here")
        self.assertEqual(kentekens.count(), 0, "db needs to be empty")
        
        print("here1")
        i1 = db2.getKentekenInfo(kentekens, '58JRNK')
        print("here2")
        expect1['_id'] = i1['_id']
        self.assertEqual(kentekens.count(), 1, "db needs have 1")
        #print(i1)
        #print(expect1)
        self.assertDictEqual(expect1, i1, "Info 1 klopt niet")    
     
        i2 = db2.getKentekenInfo(kentekens, '58JRNK')
        expect1['_id'] = i2['_id']
        self.assertEqual(kentekens.count(), 1, "db needs to have 1")
        #print(i2)
        self.assertDictEqual(expect1, i2, "Info 2 klopt niet")    
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testRdw']
    unittest.main()
