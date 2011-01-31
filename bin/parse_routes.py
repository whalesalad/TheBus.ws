#!/usr/bin/env python
# encoding: utf-8

import sys, os, csv, datetime

os.environ['DJANGO_SETTINGS_MODULE'] = 'thebus.settings'

from django.conf import settings
from thebus.ots.models import *

def main():
    route_file = settings.THEBUS_PATH+'/data/routes.txt'
    route_reader = csv.DictReader(open(route_file), delimiter=',')
    
    for row in route_reader:
        route = Route(name=row['route_long_name'],
                      short_name=row['route_short_name'],
                      ots_route_id=int(row['route_id']))
                    
        route.save()
        
        print route
        
        # print float(row['stop_lon'])

if __name__ == '__main__':
    main()
