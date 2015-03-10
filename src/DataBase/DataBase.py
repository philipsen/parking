'''
Created on Mar 6, 2015

@author: wim
'''
from pymongo.mongo_client import MongoClient
from WebScrape import WebScrape

class DataBase:
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''

    def getDb(self):
        client = MongoClient('localhost:27017')
        db = client.parkingDb
        #db.reservations.remove()
        db.reservations.create_index('key', unique=True)
        return db

    def getTestDb(self):
        client = MongoClient('localhost:27017')
        db = client.parkingDbTest
        db.reservations.remove()
        db.reservations.create_index('key', unique=True)
        db.kentekens.drop()
        db.kentekens.create_index('kenteken', unique=True)
        return db
    
    def insert(self, collection, entry):
        k = entry['key']
        collection.update({'key': k}, entry, upsert=True)
    
    def getKentekenInfo(self, kentekens, kenteken):
        #print("get info %s" % kenteken)
        f = kentekens.find({'kenteken': kenteken})
        if f.count() == 0:
            #print ("\t not in db")
            web_scrape = WebScrape.WebScrape()
            #print ("\tstart scrape")
            rdw_info = web_scrape.getRdwInfo(kenteken)
            kentekens.insert(rdw_info)
            f = kentekens.find({'kenteken': kenteken})
            assert(f.count() == 1)
        return f[0]
    
