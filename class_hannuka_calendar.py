"""
class hannuka_calendar

Pertinent state variables:
        self.python_sunsets_datetime = [] # sunsets for candlighting days in Python datetime format, timezone aware
        self.python_sunrises_datetime= [] # sunrises ending candlighting times in Python datetime format, timezone aware

Pertinent methods:
    get_candlighting_times() # returns array of times given hardcoded minchag
    get_sunrises()           # returns array of times
    get_now(self):           # returns timezone aware time at creation of object


Prepares a list of local hannukah candlelighting times for the next or current hannukah
in the given location. They are in python datetime.datetime objects, aware of local time zone.
Also prepares list of corresponding sunrises, for checking last possible candlelighting times.

Uses minchag of lighting 10 minutes after sunset for weekdays; 20 minutes before for erev shabbos.
Access the lists with object.python_candlelighting_times
                  and object.python_sunrises_datetime

Contains list of current Gregorian year's hannukah sunsets.
Methods check if current time is inside or outside of holiday, local sunset to local sunset.
    If inside, check if night time (light candles) or day time (wait to next lighting time)
Check which day within hannukah is shabbos
    If inside shabbos, wait until next lighting time after shabbos
    If before shabbos, light candles before shabbos candle lighting time, use longer-lasting candles
v. 1.  Finds local date of sunset (UTC date might be different, need local)
v. 2.  Store local date of sunset as class state variable.
v. 3.  Adds list of candlelighting times, computed for 20 minutes before sunset for erev shabbos,
        10 minutes after for weekday evenings.
v. 4.  Add finding time zone from lat/lon
v. 5.  Cleaning up extraneous print diagnostics
v. 6.  Formatted printing
TODO: Schedule the candlelighting threads
Started 19 December 2024
16 December 2025:
    Added diagnostic printing for the methods.
    Had to reload libraries, not sure why
TODO:
    Regenerate the list for the next year's holiday.
    Verify that the code works if holiday extends into January.
31 December 2025:
    Had to reload libraries again.  Might need to load them in virtual environments.
    Chanukah schedule is still the one for 2025, didn't load next years.
    Probably need to get that in Hebrew years.
    Done.
    TODO: Look for GPS receiver, adjust place/time if it is found.Else:
        Check for WiFi, adjust if that is found.
DK
"""

from pyluach.dates import HebrewDate # https://pyluach.readthedocs.io/en/latest/dates.html
from astral.sun import sun # For sunset/sunrise times.  https://sffjunkie.github.io/astral/
from astral import LocationInfo
from timezonefinder import TimezoneFinder
# from zoneinfo import ZoneInfo

import pytz # will calculate time zone from lat/lon. Use eventually for GPS timing.
#import schedule

from datetime import datetime, timedelta

from gps import gps, WATCH_ENABLE, WATCH_NEWSTYLE
import time



class hannuka_calendar:
    def __init__(self):
        # hard-code one default locationn:
        self.CWRU = LocationInfo("Glennan", "USA", "America/New_York", 41.5014728, -81.6099031)
        pos = self.find_lat_lon() # from GPS, WiFi, or default
        self.lat = pos['latitude']  # syntax for dictionary access
        self.lon = pos['longitude']
        tf = TimezoneFinder() # python package providing offline timezone lookups for WGS84 coordinates
        timezone = tf.timezone_at(lat=self.lat, lng=self.lon) # returns string such as 'Europe/Paris' or 'America/New_York'
        self.tz = pytz.timezone(timezone) # class 'pytz.tzfile.America/New_York' Zoneinfo may be better; pytz is deprecated.
        
        print('times for lat/lon', self.lat, self.lon, '\n') # work on getting city from lat/lon
        
        self.now =    datetime.now()        # in UTC; careful!
        self.now_tz = datetime.now(self.tz) # timezone aware.
        self.h_sunset_dates=[]
        self.h_sunset_datetimes=[]
        self.python_sunset_dates=[] # use this for actually determining candelighting entry point
        self.python_sunsets_datetime = [] # sunsets for candlighting days in Python datetime format, timezone aware
        self.python_sunrises_datetime= [] # sunrises ending candlighting times in Python datetime format, timezone aware
        self.find_h_and_p_sunset_dates()
        # TODO: is this the same as the above call?
        self.find_python_sunset_dates()
        self.python_candlelighting_times = [] # adjusted from sunset for erev shabbos and for weekdays
        self.find_python_candlighting_times() # fill array python_candlelighting_times

    def find_lat_lon(self):
        GPS_pos = self.get_gps_location()
        if GPS_pos != None:
            return {'source':'GPS', 'latitude':GPS_pos.lat, 'longitude':GPS_pos.lon}
        # elif WiFi_pos == None # (# insert WiFi position check here)
        else:
            print('no GPS')
            lat = self.CWRU.latitude
            lon = self.CWRU.longitude
            default_pos = {'source':'default', 'latitude':lat, 'longitude':lon}
            return default_pos
    
    def get_gps_location(self, timeout=10): # check if GPS position is available; get location if it is.
        session = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)
        start_GPS_search = time.time()

        for report in session:
            if report.get("class") != "DEVICE":
                return None # no GPS plugged in

            if (time.time()-start_GPS_search) > timeout:
                print('timed out in GPS search')
                break

            if report['class'] == 'TPV':
                lat = getattr(report, 'lat', None)
                lon = getattr(report, 'lon', None)
                if lat is not None and lon is not None:
                    return {
                        "source": "gps",
                        "lat": lat,
                        "lon": lon
                    }
        return None
    
    def find_timezone(self):
        # need code to compute time zone from position
        # if position available
            #self.tz = pytz.timezone(timezone)
        # call code that computes time and dates. For the moment, just duplicate the _init_ code here.
        pass

    # create array of datetime objects for candlelighting sunsets, hebrew and Python
    def find_h_and_p_sunset_dates(self):
        h_now=HebrewDate.today() # find today's Hebrew year.  First the Hebrew calendar day:
         # and pick out the year
        h_year=h_now.year
        # today might be after hannuka even in current Hebrew year, so check:
        if h_now > HebrewDate(h_year, 9, 24).add(days=9): # holiday is over for this year or into the next year
            # if got here, must be past chanukah for this Hebrew year (but before 1 Tishrei (rosh hashana))
            h_year += 1 # So make calculations for next Hebrew year.
        # create array of hanukkah days
        h_days = [] # candlelighting days, accounting for spill into next month
        for day in range(0,8): # holiday starts on the 25th, but need day-before sunsets, so use 24th as start day
            h_days.append(HebrewDate(h_year, 9, 24).add(days=day))
            PSD=h_days[day].to_pydate() # Python sunset date for that day
            self.python_sunset_dates.append(PSD)

    def find_python_sunset_dates(self):
        # make array of sunsets local time/dates
        for day in self.python_sunset_dates: # find sunset times corresponding to candlelighting evenings
            s = sun(self.CWRU.observer, date=day)
            sr = sun(self.CWRU.observer, date=day+timedelta(days=1))
            sset_UTC = s["sunset"] # sunset in UTC
            srise_UTC= sr["sunrise"] # sunrise in UTC
            # find correct local timezone (need local, not UTC, for Hebrew date conversion)
            sunset_local = sset_UTC.astimezone(self.tz)  # these two lines are the only tz users.  Might be able to change.
            sunrise_local= srise_UTC.astimezone(self.tz)
            self.python_sunsets_datetime.append(sunset_local)
            self.python_sunrises_datetime.append(sunrise_local)
        # diagnostic: print that array. Comment out as needed.
        # prints all 8 days of holiday sunsets for next or current Hebrew year
        # print(self.python_sunsets_datetime)
        # print(self.python_sunrises_datetime)
            
    def find_python_candlighting_times(self):
        # hard-coded minchag of lighting 20 minutes before sunset erev shabbos, 10 minutes after otherwise.
        diagnostic_print = False # True for the times to print; False otherwise
        for i in range(0, len(self.python_sunsets_datetime)):
            day_of_week = self.python_sunsets_datetime[i].strftime("%w") # 0  = Sunday; 5 = Friday
            if (day_of_week == '5'): # '5' = Friday, erev shabbos
                self.python_candlelighting_times.append(self.python_sunsets_datetime[i] - timedelta(minutes=20))
                if (diagnostic_print):
                    formatted_output = self.python_candlelighting_times[i].strftime("%Y-%m-%d %H:%M")
                    print('Candle ', i+1, f'{formatted_output} (earlier for erev shabbos)')
            else: # weekday
                self.python_candlelighting_times.append(self.python_sunsets_datetime[i] + timedelta(minutes=10))
                if (diagnostic_print):
                    formatted_output = self.python_candlelighting_times[i].strftime("%Y-%m-%d %H:%M")
                    print('Candle ', i+1, f'{formatted_output}')
            # print('corresponding sunrise: ', self.python_sunrises_datetime[i])
            
    def get_candlighting_times(self):
        return self.python_candlelighting_times
    
    def get_sunrises(self):
        return self.python_sunrises_datetime
    
    def get_now(self): # returns timezone aware time at creation of object
        return self.now_tz
        
        
if __name__ == '__main__':
    hc = hannuka_calendar()
    cl_times = hc.get_candlighting_times()
    for date in cl_times:
        print('candlelighting times from getter method:', date)
    print('\n')

    sr_times = hc.get_sunrises()
    for date in sr_times:
        print('sunrise times from getter method:', date)
        
    now_tz = hc.get_now()
    print('\ncurrent time from getter method: ', now_tz)
    
    print('get_gps_location: ', hc.get_gps_location())