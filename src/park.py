'''
Created on Mar 6, 2015

@author: wim

Retrieve usages of the parking cards from the website of Delft parking. 
Add data to the database

'''

from WebScrape import WebScrape
from DataBase import DataBase
import config
from config import nummers

if __name__ == '__main__':
    
    nummers = config.nummers
     
    database = DataBase.DataBase()
    reservations = database.getDb().reservations
    print("db has %d entries" % reservations.count())
    
    scrape = WebScrape.WebScrape()
    
    for n in nummers:
        print "n = ", n
        (rem, res) = scrape.getHistory(n['nr'], n['pin'])
        print "res2=", res
        for r in res:
            proc_item = scrape.procItem(r, n['name'])
            database.insert(reservations, proc_item)
        print("db has %d entries" % reservations.count())
        print ("remaining on this card = ", rem)
        
