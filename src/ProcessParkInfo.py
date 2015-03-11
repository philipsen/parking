'''
Created on Mar 7, 2015

@author: wim
'''
from database import DataBase
from Reservation import Reservation

if __name__ == '__main__':
    
    database = DataBase.DataBase()
    reservations = database.get_db().reservations
    kentekens = database.get_db().kentekens
   
    print("Er zijn %d gebruiken geregistreerd" % reservations.count()) 
    total_minutes = 0.0
    for r in reservations.find().sort('start'):
        #print r
        reservation = Reservation(r)
        total_minutes += reservation.calcMinutes()
        print reservation
    print("Totaal gebruikt %d uur %d minuten" % (int(total_minutes / 60), (total_minutes % 60)))
    p = total_minutes / ((408 + 360) * 60) * 100
    pt = 100 * 8.0 / (365 - 31 - 28)
    print("{:0.2f}% van de uren gebruikt in {:0.2f}% van de dagen".format(p, pt))
