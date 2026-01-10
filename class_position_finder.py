"""
Class to find position and set Pi clock
If GPS receiver present, use that.
Else use WiFi
Else use default (need to figure out Pi clock setting; Pi 5 has real-time clock)

Started 3 January 2026
TODO: Get GPS position and time.
      Add get_time() method, or method for setting Pi clock time to GPS.
DK
"""

from gps import gps, WATCH_ENABLE, WATCH_NEWSTYLE
from astral import LocationInfo
from timezonefinder import TimezoneFinder

import time
import os
#from zoneinfo import ZoneInfo
#import pytz # will calculate time zone from lat/lon. Use eventually for GPS timing.


class position_finder:
    
    def __init__(self):
        # set default location
        self.CWRU = LocationInfo("Glennan", "USA", "America/New_York", 41.5014728, -81.6099031)
        self.lat = self.CWRU.latitude
        self.lon = self.CWRU.longitude
        self.tf = TimezoneFinder()
        self.timezone = self.tf.timezone_at(lat=self.lat, lng=self.lon)
        self.default_pos = {'source':'default', 'lat': self.CWRU.latitude, 'lon': self.CWRU.longitude, "timezone": self.timezone}        
        
    def _gps_status(self, timeout=5): # reports Boolean of gps_OK/not_OK/OK_but_no_time
        session = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)
        start = time.monotonic()
        device = False
        time_seen = False

        while time.monotonic() - start < timeout:
            try:
                report = session.next()
            except Exception:
                time.sleep(0.1)
                continue

            if not report:
                continue

            cls = report.get("class")

            if cls == "DEVICE":
                device = True

            if cls == "TPV" and report.get("time"):
                time_seen = True

        if time_seen:
            return "gps_ok"
        if device:
            return "device_present_no_time"
        return "no_gps"
    
    

    def _gps_possible(self):
        return any(os.path.exists(p) for p in (
            "/dev/ttyUSB0", "/dev/ttyACM0", "/dev/serial0"
        ))

    def _get_gps_location(self, timeout=10): # check if GPS position is available; get location if it is.
        session = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)
        start_GPS_search = time.time()

        for report in session:
            if (time.time()-start_GPS_search) > timeout:
                print('timed out in GPS search')
                return None # timed out, no fix

            if report.get('class') != 'TPV':
                continue
            
            lat = report.get('lat')
            lon = report.get('lon')
            
            if lat is not None and lon is not None:
                tf = TimezoneFinder()
                timezone = tf.timezone_at(lat=lat, lng=lon) # works; need the full statement of arguments

                return {
                    "source": "gps",
                    "lat": lat,
                    "lon": lon,
                    "timezone": timezone
                }

        return None

    def get_position(self): # returns a dictionary source, lat, lon, timezone
        if self._gps_possible():
            return self._get_gps_location()
        else:
            return self.default_pos
    
    
if __name__ == '__main__':
    print('class position_finder test code')
    pf = position_finder()
    position_dictionary = pf.get_position()
    
    print('pf.get_position: ',position_dictionary , '\n') # works for case GPS present.  Check without GPS.
    print('\nExample of reading from dictionary:')
    print('source is: ', position_dictionary['source'])
