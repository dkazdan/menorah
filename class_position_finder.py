"""
Class to find position and set Pi clock
If GPS receiver present, use that.
Else use WiFi
Else use default (need to figure out Pi clock setting; Pi 5 has real-time clock)

Started 3 January 2026
TODO: Get GPS position and time.
      Add get_time() method.
DK
"""

import pytz # will calculate time zone from lat/lon. Use eventually for GPS timing.
#import schedule

from datetime import datetime, timedelta

from gps import gps, WATCH_ENABLE, WATCH_NEWSTYLE
from astral import LocationInfo
from timezonefinder import TimezoneFinder
from zoneinfo import ZoneInfo
import pytz # will calculate time zone from lat/lon. Use eventually for GPS timing.


import time


class position_finder:
    
    def __init__(self):
        # set default location
        self.CWRU = LocationInfo("Glennan", "USA", "America/New_York", 41.5014728, -81.6099031)
        self.lat = self.CWRU.latitude
        self.lon = self.CWRU.longitude
        tf = TimezoneFinder()
        timezone = tf.timezone_at(lat=self.lat, lng=self.lon)
        print('lat: ', self.lat, 'lon: ', self.lon, 'timezone: ', timezone)
    
    def get_position(self): # returns tuple of lat lon
        return self.lat, self.lon
    
    
if __name__ == '__main__':
    print('test code')
    pf = position_finder()
    print(pf.get_position())