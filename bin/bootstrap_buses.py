#!/usr/bin/env python
# encoding: utf-8

import sys, os, time, math, urllib
from thebus.ots.models import *

os.environ['DJANGO_SETTINGS_MODULE'] = 'thebus.settings'

for r in range(854, 868):
    bus = Bus(number=r, length="M", paint="R", manufacturer="G", model="Phantom")
    bus.save()

for r in range(501, 555):
    bus = Bus(number=r, length="M", paint="R", manufacturer="G", model="Low Floor")
    bus.save()

for r in range(116, 131):
    bus = Bus(number=r, length="L", paint="R", manufacturer="N", model="D60LF")
    bus.save()
    
for r in range(132, 141):
    bus = Bus(number=r, length="L", paint="X", manufacturer="N", model="DE60LF", hybrid=True)
    bus.save()

for r in range(901, 940):
    bus = Bus(number=r, length="M", paint="R", manufacturer="N", model="DE40LFR", hybrid=True)
    bus.save()

for r in range(142, 160):
    bus = Bus(number=r, length="L", paint="R", manufacturer="N", model="DE60LFR", hybrid=True)
    bus.save()