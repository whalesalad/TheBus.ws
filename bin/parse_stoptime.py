#!/usr/bin/env python
# encoding: utf-8

import sys, os, csv, datetime

sys.path.append('/home/michael/sites')
os.environ['DJANGO_SETTINGS_MODULE'] = 'thebus.settings'

from django.conf import settings
from thebus.ots.models import *

def main():
    stoptime_file = settings.THEBUS_PATH+'/data/stop_times.txt'
    stoptime_reader = csv.DictReader(open(stoptime_file), delimiter=',')
    
    for row in stoptime_reader:
        stop = Stop.objects.get(ots_stop_id=row['stop_id'])
        trip = Trip.objects.get(ots_trip_id=row['trip_id'])
        
        st = StopTime(stop=stop, trip=trip, ots_trip_id=row['trip_id'], ots_stop_id=row['stop_id'])
        
        st.save()
        
        print "====[ New StopTime with ID %s ]============" % (st.id,)
        print "Saved for stop %s" % (stop.name,)
        print
        # print st

if __name__ == '__main__':
    main()
