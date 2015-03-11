'''
Created on Mar 6, 2015
@author: wim
'''
from pymongo.mongo_client import MongoClient
from webscrape import webscrape
import logging

class DataBase(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.debug = False

    @staticmethod
    def get_db():
        '''
        return mongo collection
        '''
        #print "get_db"
        client = MongoClient('localhost:27017')
        database = client.parkingDb
        #database.reservations.remove()
        database.reservations.create_index('key', unique=True)
        return database

    @staticmethod
    def get_test_db():
        '''
        return the test collection
        '''
        #print "get_test_db"
        client = MongoClient('localhost:27017')
        database = client.parkingDbTest
        database.reservations.remove()
        database.reservations.create_index('key', unique=True)
        database.kentekens.drop()
        database.kentekens.create_index('kenteken', unique=True)
        return database

    @staticmethod
    def insert(collection, entry):
        '''
        insert a entry into the given collection
        '''
        logging.info("insert")
        k = entry['key']
        collection.update({'key': k}, entry, upsert=True)

    @staticmethod
    def get_kenteken_info(kentekens, kenteken):
        '''
        return info
        '''
        #print "get info %s" % kenteken
        qres = kentekens.find({'kenteken': kenteken})
        if qres.count() == 0:
            #print ("\t not in db")
            web_scrape = webscrape.WebScrape()
            #print ("\tstart scrape")
            rdw_info = web_scrape.get_rdw_info(kenteken)
            kentekens.insert(rdw_info)
            qres = kentekens.find({'kenteken': kenteken})
            assert qres.count() == 1
        return qres[0]

