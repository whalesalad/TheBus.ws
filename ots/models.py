from django.db import models

import geopy.distance
import geopy.units
from geopy import geocoders

from thebus.ots.hea import *

class Route(models.Model):
    
    """
    This model describes a bus route
    
    Ewa Beach-Waikiki,3,,1,28,,,,42
    
    route_long_name: Ewa Beach-Waikiki
    route_type: 3
    route_text_color: None
    agency_id: 1
    route_id: 28
    route_color: None
    route_desc: None
    route_url: None
    route_short_name: 42
    
    """
    
    name = models.CharField(max_length=100)
    short_name = models.CharField(unique=True, null=False, max_length=4)
    
    # OTS Fields
    ots_route_id = models.IntegerField(unique=True, null=False)
    
    def __str__(self):
        return self.short_name

class StopManager(models.Manager):
    def __init__(self):
        super(StopManager, self).__init__()
  
    def near(self, latitude=None, longitude=None, distance=None):
        if not (latitude and longitude and distance):
            return []

        queryset = super(StopManager, self).get_query_set()

        # prune down the set of all locations to something we can quickly check precisely
        # my location: 21.304983,-157.835936
        rough_distance = geopy.units.degrees(arcminutes=geopy.units.nm(miles=0.5)) * 1
        
        queryset = queryset.filter(
              latitude__range=(latitude - rough_distance, latitude + rough_distance),
              longitude__range=(longitude - rough_distance, longitude + rough_distance)
              )

        stops = []
        for stop in queryset:
            stop.rough_distance = rough_distance
            if stop.latitude and stop.longitude:
                exact_distance = geopy.distance.distance((latitude, longitude), (stop.latitude, stop.longitude))
            if exact_distance.miles < distance:
                stop.miles = exact_distance
                stop.distance = int(math.floor(exact_distance.feet))
                stops.append(stop)
        
        close_locations = sorted(stops, lambda x,y: cmp(x.miles.feet, y.miles.feet))[:20]
        
        # queryset = queryset.filter(id__in=[s.id for s in close_locations])
        return close_locations

class Stop(models.Model):
    
    """
    This model describes a bus stop
    
    21.304998,2088,-157.835904,2088,http://hea.thebus.org/nextbus.asp?s=2088,,,KEEAUMOKU ST + WILDER AVE,0,
    
    stop_code: 2088
    stop_lat: 21.304998
    stop_lon: -157.835904
    stop_id: 2088
    stop_url: http://hea.thebus.org/nextbus.asp?s=2088
    parent_station: None
    stop_desc: None
    stop_name: KEEAUMOKU ST + WILDER AVE
    location_type: 0
    zone_id: None
    
    """
    
    DIRECTION_CHOICES = (
        (u'N', u'Northbound'),
        (u'S', u'Southbound'),
        (u'W', u'Westbound'),
        (u'E', u'Eastbound'),
    )
    
    code = models.PositiveIntegerField(null=False, unique=True, help_text="This is the offical TheBus stop code.")
    latitude = models.FloatField()
    longitude = models.FloatField()
    hea_url = models.URLField(default="http://hea.thebus.org", help_text="This is the URL to the HEA page for the bus stop.")
    name = models.CharField(max_length=100, null=False)
    routes = models.ManyToManyField(Route)
    direction = models.CharField(max_length=1, choices=DIRECTION_CHOICES, null=True)
    
    # OTS Fields
    ots_stop_id = models.IntegerField(unique=True, null=False)
    
    objects = StopManager()
    
    @property
    def get_routes(self):
        routes = self.routes.all().order_by('short_name')

        if not routes:
            self.routes = self.get_distinct_routes
            self.save()
            return self.routes.all().order_by('short_name')
        
        return routes
        
    @property
    def route_string(self):
        routes = self.get_routes
        
        route_string = []
        for r in routes[:5]:
            route_string.append(r.short_name)
        
        if len(routes) > 5:
            short_route_length = len(routes)-5
            route_string.append("and %s more" % short_route_length)
            
        return ", ".join(route_string)
        # return "MEOW"
        
    
    @property
    def get_distinct_routes(self):
        stoptimes = StopTime.objects.filter(stop=self)
        
        seen = set()
        keepers = []
        
        for stoptime in stoptimes: 
            route = stoptime.trip.route
            route_num = route.short_name
        
            if not route_num in seen:
                seen.add(route_num) 
                keepers.append(route)
        
        return keepers
    
    
    @property
    def get_times(self):
        try:
            hea = HEA(self.code)
            
            if not self.direction:
                hea_direction = hea.get_stop_direction()

                if hea_direction:
                    for direction in self.DIRECTION_CHOICES:
                        if hea_direction == direction[1]:
                            self.direction = direction[0]
                            self.save()

            return hea.get_items()

        except:
            return False
        
    
    @models.permalink
    def get_absolute_url(self):
        return ('thebus.web.views.stop_detail', [str(self.code)])
    
    @property
    def map_url(self):
        return "http://maps.google.com/?q=%s,%s" % (self.latitude, self.longitude)
    
    @property
    def short_direction(self):
        directions = {
            'E': 'East',
            'W': 'West'
        }
        
        return directions.get(self.direction, 'E')
    
    @models.permalink
    def get_nearby_stops_url(self):
        return ('thebus.web.views.search_by_location', [str(self.latitude), str(self.longitude)])
        # return '/location?lat=%s&long=%s' % (self.latitude, self.longitude,)

class Trip(models.Model):
    
    """
    Each route has certain trips
    
    block_id: a_43203
    route_id: 2
    direction_id: 0
    trip_headsign: SCHOOL STREET - Middle Street
    service_id: 804
    trip_id: 228055
    
    """
    
    headsign = models.CharField(max_length=100)
    route = models.ForeignKey('Route')
    
    # OTS Fields
    ots_route_id = models.IntegerField(null=False)
    ots_trip_id = models.IntegerField(unique=True, null=False)


class StopTime(models.Model):
    
    """
    Connects a trip to a stop, this is the big daddy database.
    
    trip_id: 228055
    arrival_time: 13:55:00
    departure_time: 13:55:00
    stop_id: 12
    stop_sequence: 1
    
    stop_headsign:
    pickup_type:
    drop_off_type:
    shape_dist_traveled:

    """
    
    trip = models.ForeignKey('Trip')
    stop = models.ForeignKey('Stop')
    
    # OTS Fields
    ots_trip_id = models.IntegerField(null=False)
    ots_stop_id = models.IntegerField(null=False)
    
    
class Bus(models.Model):
    """
    A Bus Model :D
    """
    
    LENGTH_CHOICES = (
        (u'S', u'30\''),
        (u'M', u'40\''),
        (u'L', u'60\' (Articulating)'),
    )
    
    PAINT_CHOICES = (
        (u'S', u'Standard'),
        (u'R', u'Rainbow'),
        (u'X', u'Silver'),
    )
    
    MANUF_CHOICES = (
        (u'G', u'Gillig'),
        (u'N', u'New Flyer'),
    )
    
    number = models.IntegerField(null=False, unique=True)
    length = models.CharField(max_length=1, choices=LENGTH_CHOICES, null=True, default='M')
    paint = models.CharField(max_length=1, choices=PAINT_CHOICES, null=True, default='S')
    manufacturer = models.CharField(max_length=1, choices=MANUF_CHOICES, null=True, default='G')
    model = models.CharField(max_length=100, null=True)
    is_hybrid = models.BooleanField(help_text="Is this a Hybrid bus?")
    
    class Meta:
        verbose_name_plural = 'buses'
    
    @property
    def model_string(self):
        return '%s %s %s' % (self.get_length_display(), self.get_manufacturer_display(), self.model)