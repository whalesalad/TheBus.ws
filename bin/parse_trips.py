#!/usr/bin/env python
# encoding: utf-8

import sys, os, csv, datetime

os.environ['DJANGO_SETTINGS_MODULE'] = 'thebus.settings'

from django.conf import settings
from thebus.ots.models import *

def main():
    trips_file = settings.THEBUS_PATH+'/data/trips.txt'
    trips_reader = csv.DictReader(open(trips_file), delimiter=',')
    
    for row in trips_reader:
        route = Route.objects.get(ots_route_id=row['route_id'])
        
        trip = Trip(headsign=row['trip_headsign'],
                    route=route,
                    ots_route_id=int(row['route_id']),
                    ots_trip_id=int(row['trip_id']))
                    
        trip.save()
        
        print trip

if __name__ == '__main__':
    main()
