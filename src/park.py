'''
Created on Mar 6, 2015

@author: wim

Retrieve usages of the parking cards from the website of Delft parking.
Add data to the database

'''

from webscrape import webscrape
from database import database
import config
#from config import nummers

if __name__ == '__main__':
    nummers = config.nummers
    db2 = database.DataBase()
    reservations = db2.get_db().reservations
    print "db has %d entries" % reservations.count()
    scrape = webscrape.WebScrape("firefox")
    for n in nummers:
        print "n = ", n
        (rem, res) = scrape.get_history(n['nr'], n['pin'])
        print "res2=", res
        for r in res:
            proc_item = scrape.proc_item(r, n['name'])
            if proc_item is not None:
                db2.insert(reservations, proc_item)
        print "db has {0} entries".format(reservations.count())
        print "remaining on this card = {0}".format(rem)
