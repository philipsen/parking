'''
Created on Mar 7, 2015

@author: wim
'''
from datetime import datetime
from database import database

class Reservation(object):
    '''
    classdocs
    '''
    def __init__(self, r):
        '''
        Constructor
        '''
        self.dict = r

    def calc_minutes(self):
        '''
        calculate the duration of this reservation
        '''
        start = datetime.strptime(self.dict['start'], "%d-%m-%Y %H:%M")
        end = datetime.strptime(self.dict['end'], "%d-%m-%Y %H:%M")
        dur = end - start
        return dur.total_seconds() / 60

    def __str__(self):
        ''' print it '''
        db2 = database.DataBase()
        kentekens = db2.get_db().kentekens
        kenteken_info = db2.get_kenteken_info(kentekens, self.dict['kenteken'])
        return '%s\t%s\t%d\t%s\t%s, %s' % (self.dict['start'], self.dict['kenteken'],
                                           self.calc_minutes(), kenteken_info['kleur'],
                                           kenteken_info['merk'], kenteken_info['naam'])
