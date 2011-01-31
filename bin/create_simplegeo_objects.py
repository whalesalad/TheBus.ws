#!/usr/bin/env python
# encoding: utf-8

import sys, os, time, math, urllib, simplegeo
from thebus.ots.models import *

os.environ['DJANGO_SETTINGS_MODULE'] = 'thebus.settings'

import thebus.settings as settings

sg_client = simplegeo.Client(settings.SIMPLEGEO_TOKEN, settings.SIMPLEGEO_SECRET)
sg_layer = 'thebus'

stops = Stop.objects.all()

records = []

for s in stops:
    r = simplegeo.Record(layer=sg_layer, id=s.id, lat=s.latitude, lon=s.longitude)
    print '==============================='
    print 'Adding Record for Stop #%s' % (s.code)
    print
    sg_client.add_record(r)

# sg_client.add_records(sg_layer, records)

# print sg_client.get_layer_stats('thebus')