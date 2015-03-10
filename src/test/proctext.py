'''
Created on Mar 6, 2015

@author: wim
'''

import unittest
from DataBase import DataBase
from WebScrape import WebScrape

class Test(unittest.TestCase):

    def testProcText(self):
        print ("testProcText")
        res = ['04-03-2015 16:54\n04-03-2015 17:24\n63HFLD\n30 min',
               '04-03-2015 13:31\n04-03-2015 14:31\n74HST7\n1 uur', 
               '04-03-2015 10:00\n04-03-2015 10:29\n6VXR12\n30 min', 
               '04-03-2015 10:00\n04-03-2015 10:27\nVN984D\n28 min', 
               '02-03-2015 20:37\n02-03-2015 23:02\n58JRNK\n2 uur 25 min', 
               '02-03-2015 19:52\n02-03-2015 23:12\n67JLF9\n3 uur 20 min', 
               '02-03-2015 19:43\n02-03-2015 20:43\n58JRNK\n1 uur', 
               '02-03-2015 19:41\n02-03-2015 19:43\n58JRNK\n2 min']
                
        web_scrape = WebScrape.WebScrape()
        db2 = DataBase.DataBase()
        db = db2.getTestDb()
        reservations = db.reservations
        count = reservations.count()

        self.assertEqual(count, 0, "db needs to be empty")

        for r in res:
            proc_item = web_scrape.procItem(r, 2) 
            db2.insert(reservations, proc_item)
            #reservations.insert(proc_item)
        
        count = reservations.count()
        print("db has %d entries" % count)
        self.assertEqual(count, 8, "db needs 8 entries")

        for r in res:
            proc_item = web_scrape.procItem(r, 1)
            db2.insert(reservations, proc_item)
            #reservations.insert(proc_item)
        
        count = reservations.count()
        print("db has %d entries" % count)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testProcText']
    unittest.main()
