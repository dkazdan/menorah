"""
Class for determining time of next menorah lighting.
Finds entry time as datetime.now
Follows decision tree to determine whether to light candles immediately
  or to wait for next candlelighting time.
Finds number of candles to be lit then.

TODO: Fill in decision tree for lighting now or later.  Include shabbos and weekday sunrise.
"""

import schedule
from datetime import datetime
from astral import LocationInfo
from timezonefinder import TimezoneFinder
from zoneinfo import ZoneInfo
import pytz # will calculate time zone from lat/lon. Use eventually for GPS timing.

from class_hannuka_calendar import hannuka_calendar

class candle_scheduler:
    
    def __init__(self):
        # TODO: Get all of this into position/timezone object
        self.CWRU = LocationInfo("Glennan", "USA", "America/New_York", 41.5014728, -81.6099031)
        self.lat = self.CWRU.latitude
        self.lon = self.CWRU.longitude
        tf = TimezoneFinder()
        # TODO: Set lat/lon by GPS; have method for setting lat/lon externally
        timezone = tf.timezone_at(lat=self.lat, lng=self.lon)
        tz = pytz.timezone(timezone) # type str
        now = datetime.now(pytz.utc)
        self.now_local = now.astimezone(tz)
        print('now.local: ', self.now_local)

        self.starting_datetime = datetime.now()
        self.next_lighting_time = datetime.now() # placeholder; will modify
        self.next_number_of_candles = 1 # plus shammash.  Most likely start
        self.next_burn_time = 40 # minutes; will make longer for shabbos
        self.h_c = hannuka_calendar()
        # for program entry:
        # get list of previous candlelighting time (or None) and next.
        # Check previous one against following dawn on weekdays;
        # current sunset if shabbos
        # to decide if should light now or wait until next candelighting time.
        self.next_time_list = self.find_previous_and_next_lighting_time()
        print('previous lighting time: ', self.next_time_list[0], 'Next lighting time: ', self.next_time_list[1])
        print('next lighting time: ', self.find_next_lighting_time())
        print('should light candles now: ', self.should_light_now())
    # return list of previous candlighting time (or None) and next.
    def find_previous_and_next_lighting_time(self):
        previous_lighting_time = None
        next_lighting_time = None
        time_list = []
        for time in self.h_c.python_candlelighting_times:
            if time > self.now_local: # if next time on list is after now, likely light at time on list.
                next_lighting_time = time
                time_list = [previous_lighting_time, next_lighting_time]
                return time_list # and drop out of the loop
            else: # but check on previous time--might still be within bounds for it.
                #if previous_lighting_time != None:
                previous_lighting_time = time
    # return list of previous candlighting time (or None) and next.
    def find_next_lighting_time(self):
        for time in self.h_c.python_candlelighting_times:
            if time > self.now_local: # if next time on list is after now, likely light at time on list.
                next_lighting_time = time
                return time # and drop out of the loop
            
    def should_light_now(self): # Returns true if can light candle right now; false if should wait to next candelighting time
        # TODO: Fill in decision tree here
        return True
    
if __name__ == "__main__":
    cs = candle_scheduler()