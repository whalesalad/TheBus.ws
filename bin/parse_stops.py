#!/usr/bin/env python
# encoding: utf-8

import sys, os, csv, datetime

os.environ['DJANGO_SETTINGS_MODULE'] = 'thebus.settings'

from django.conf import settings
from thebus.ots.models import *

def main():
    stop_file = settings.THEBUS_PATH+'/data/stops.txt'
    stop_reader = csv.DictReader(open(stop_file), delimiter=',')
    
    # code = models.PositiveIntegerField(null=False, unique=True, help_text="This is the offical TheBus stop code.")
    # latitude = models.DecimalField(max_digits=8, decimal_places=6)
    # longitude = models.DecimalField(max_digits=8, decimal_places=6)
    # hea_url = models.URLField(default="http://hea.thebus.org", help_text="This is the URL to the HEA page for the bus stop.")
    # name = models.CharField(max_length=100, null=False)
    # ots_stop_id
    
    # {
    # 'stop_lat': '21.370954', 
    # 'stop_code': '479', 
    # 'stop_lon': '-157.933992', 
    # 'stop_id': '479', 
    # 'stop_url': 'http://hea.thebus.org/nextbus.asp?s=479', 
    # 'parent_station': '', 
    # 'stop_desc': '', 
    # 'stop_name': 'KAMEHAMEHA HWY + SALT LAKE BL', 
    # 'location_type': '0', 
    # 'zone_id': ''}
    
    
    for row in stop_reader:
        stop = Stop(code=int(row['stop_code']), 
                    latitude=float(row['stop_lat']), 
                    longitude=float(row['stop_lon']), 
                    hea_url=row['stop_url'],
                    name=row['stop_name'],
                    ots_stop_id=int(row['stop_id']))
                    
        stop.save()
        
        print stop
        
        # print float(row['stop_lon'])

if __name__ == '__main__':
    main()
