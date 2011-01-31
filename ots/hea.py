import sys, os, time, math, urllib, re
from elementtree.ElementTree import parse
from BeautifulSoup import BeautifulSoup

# http://hea.thebus.org/getBus.asp?t=1266230076&s=46&r=
# The time is the from Date.parse(Date()) in JS, which is seconds from the unix epoch, with the last 3 seconds cut off

class TimeItem(object):
    """
    This is a time item
    <li><a href="nextbus.asp?s=306&amp;r=4"><b>4 NUUANU - Dowsett Avenue via UH Manoa</b><br /><i>Westbound<br />scheduled (no GPS) &#183; 5:46 AM</i></a></li>
    """
    
    def __init__(self, html):
        # parse the html into attributes like
        # 
        self.contents = html.contents[0].contents
        
        timeinfo = self.contents[2]
        
        self.name = self.contents[0].string
        self.direction = timeinfo.contents[0]
        self.time = timeinfo.contents[2]
    
    def display(self):
        print "=================================="
        print "ROUTE: %s" % (self.name)
        print "DIRECTION: %s" % (self.direction)
        print "TIME: %s" % (self.time)
        print


class HEA(object):
    """
    Passed a stop ID, get the specific time's for that stop
    """
    
    def __init__(self, stop_code):
        items = self.get_hea_payload(stop_code)
        
        self.items = []
        
        for item in items:
            self.items.append(TimeItem(item))
        
    def get_items(self):
        return self.items
    
    def get_stop_direction(self):
        return self.items[0].direction
    
    def get_hea_payload(self, stop):
        params = urllib.urlencode({
            't': int(math.ceil(time.time())),
            's': stop,
        })
        
        url = "http://hea.thebus.org/getBus.asp?%s" % (params)
        
        self.payload = urllib.urlopen(url)
        
        tree = parse(self.payload)
        description = tree.find('description')
        
        soup = BeautifulSoup(description.text)
        
        return soup.contents[0].contents


# USAGE
# items = get_hea_payload(393)
# 
# for item in items:
#     i = TimeItem(item)
#     i.display()