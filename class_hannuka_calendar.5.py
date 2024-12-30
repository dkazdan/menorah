"""
class hannuka_calendar

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
v. 1.	Finds local date of sunset (UTC date might be different, need local)
v. 2.	Store local date of sunset as class state variable.
v. 3.	Adds list of candlelighting times, computed for 20 minutes before sunset for erev shabbos,
        10 minutes after for weekday evenings.
v. 4.	Add finding time zone from lat/lon
v. 5.	Cleaning up extraneous print diagnostics
TODO: Schedule the candlelighting threads
Started 19 December 2024
DK
"""

from pyluach.dates import HebrewDate # https://pyluach.readthedocs.io/en/latest/dates.html
from astral.sun import sun # https://sffjunkie.github.io/astral/
from astral import LocationInfo
from  timezonefinder import TimezoneFinder
from zoneinfo import ZoneInfo

import pytz # will calculate time zone from lat/lon. Use eventually for GPS timing.
#import schedule

from datetime import datetime, timedelta



class hannuka_calendar:
    def __init__(self):
        self.CWRU = LocationInfo("Glennan", "USA", "America/New_York", 41.5014728, -81.6099031)
        self.lat = self.CWRU.latitude
        self.lon = self.CWRU.longitude
        tf = TimezoneFinder()
        # TODO: Set lat/lon by GPS; have method for setting lat/lon externally
        timezone = tf.timezone_at(lat=self.lat, lng=self.lon)
        self.tz = pytz.timezone(timezone) # type str
        self.now=datetime.now() # will be in UTC; careful!
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
        
    # create array of datetime objects for candlelighting sunsets
    def find_h_and_p_sunset_dates(self):
        # find today's Hebrew year.
        h_now=HebrewDate.today()
        h_year=h_now.year
        # might be after hannuka in current Hebrew year, so check:
        if h_now > HebrewDate(h_year, 9, 24).add(days=9): # holiday is over for this year
            h_now += 1 # so get ready for next year.
        # create array of hanukkah days
        h_days = [] # candlelighting days, accounting for spill into next month
        for day in range(0,8):
            h_days.append(HebrewDate(h_year, 9, 24).add(days=day))
            PSD=h_days[day].to_pydate()
            self.python_sunset_dates.append(PSD)

    def find_python_sunset_dates(self):
        # make array of sunsets local time/dates
        for day in self.python_sunset_dates: # find sunset times corresponding to candlelighting evenings
            s = sun(self.CWRU.observer, date=day)
            sr = sun(self.CWRU.observer, date=day+timedelta(days=1))
            sset_UTC = s["sunset"] # sunset in UTC
            srise_UTC= sr["sunrise"] # sunrise in UTC
            # find correct local timezone (need local, not UTC, for Hebrew date conversion)
            sunset_local = sset_UTC.astimezone(self.tz)
            sunrise_local= srise_UTC.astimezone(self.tz)
            self.python_sunsets_datetime.append(sunset_local)
            self.python_sunrises_datetime.append(sunrise_local)
            
    def find_python_candlighting_times(self):
        # hard-coded minchag of lighting 20 minutes before sunset erev shabbos, 10 minutes after otherwise.
        for i in range(0, len(self.python_sunsets_datetime)):
            day_of_week = self.python_sunsets_datetime[i].strftime("%w") # 0  = Sunday; 5 = Friday
            if (day_of_week == '5'): # '5' = Friday, erev shabbos
                self.python_candlelighting_times.append(self.python_sunsets_datetime[i] - timedelta(minutes=20))
                print('python_candlelighting_times: ', self.python_candlelighting_times[i], '(erev shabbos)')
            else: # weekday
                self.python_candlelighting_times.append(self.python_sunsets_datetime[i] + timedelta(minutes=10))
                print('python_candlelighting_times: ', self.python_candlelighting_times[i])
            print('corresponding sunrise: ', self.python_sunrises_datetime[i])
        
if __name__ == '__main__':
    hc = hannuka_calendar()
