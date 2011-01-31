from django.db import models
from django.contrib.localflavor.us.us_states import STATE_CHOICES

import geopy.distance
from geopy import geocoders

class StopManager(models.Manager):
    def __init__(self):
        super(StopManager, self).__init__()
  
    def near(self, latitude=None, longitude=None, distance=None):
        if not (latitude and longitude and distance):
            return []

        queryset = super(StopManager, self).get_query_set()

        # prune down the set of all locations to something we can quickly check precisely
        rough_distance = geopy.distance.arc_degrees(arcminutes=geopy.distance.nm(miles=distance)) * 2
        queryset = queryset.filter(
              latitude__range=(latitude - rough_distance, latitude + rough_distance),
              longitude__range=(longitude - rough_distance, longitude + rough_distance)
              )

        locations = []
        for location in queryset:
            if location.latitude and location.longitude:
                exact_distance = geopy.distance.distance(
                          (latitude, longitude),
                          (location.latitude, location.longitude)
                          )
            exact_distance.calculate()
            if exact_distance.miles <= distance:
                locations.append(location)

        queryset = queryset.filter(id__in=[l.id for l in locations])
        return queryset
