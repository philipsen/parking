'''
Created on Mar 7, 2015

@author: wim
'''
from database import database
from Reservation import Reservation

if __name__ == '__main__':

    db2 = database.DataBase()
    reservations = db2.get_db().reservations
    kentekens = db2.get_db().kentekens

    print "Er zijn %d gebruiken geregistreerd" % reservations.count()
    total_minutes = 0.0
    for r in reservations.find().sort('start'):
        print "r = {0}".format(r)
        reservation = Reservation(r)
        total_minutes += reservation.calc_minutes()
        print reservation
    print "Totaal gebruikt %d uur %d minuten" % (int(total_minutes / 60), (total_minutes % 60))
    p = total_minutes / ((408 + 360) * 60) * 100
    pt = 100 * 8.0 / (365 - 31 - 28)
    print "{:0.2f}% van de uren gebruikt in {:0.2f}% van de dagen".format(p, pt)
