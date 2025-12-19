"""
class Menorah
Entry point for program.
Finds time and position plus time zone.
Obtains vector of candlelighting times and of corresponding sunrises.
Checks state of holiday at starting time per starting_time enum.
Manages schedule for next candlelighting.
Started 18 December 2025
DK
"""


from enum import Enum, auto # auto() numers the values sequentially
from datetime import datetime, timedelta
from class_hannuka_calendar import hannuka_calendar



class Menorah:
    
    class starting_time(Enum):
        BEFORE_HOLIDAY = auto()                        # light at time of next (i.e., first) candle
        BETWEEN_LIGHTING_AND_SUNRISE = auto()          # light immediately
        BETWEEN_LIGHTING_AND_SUNRISE_SHABBOS = auto()  # light at time of next candle
        AFTER_SUNRISE = auto()                         # light at time of next candle
        
    
    def __init__(self):
        self.start = self.starting_time.BEFORE_HOLIDAY
        self.current_time_utc = datetime.now()
        self.hc = hannuka_calendar()
        self.cl_times = self.hc.get_candlighting_times()
        self.sr_times = self.hc.get_sunrises()
        self.now_tz =   self.hc.get_now()
        print(self.now_tz)
        #self.current_time = hc.get_now()
        # get timezone from class_hannuka_calendar; make current time timezone aware
        #self.current_time_utc = datetime.now(timezone.utc)
        
    def is_now_before_first_candle(self):
        return self.now_tz < self.cl_times[0]
    
    def is_now_after_last_sunrise(self):
        return self.now_tz > self.sr_times[7]
    
    def is_during_lighting_time(self): # after a candlighting time but before sunrise.
        for i, (cl, sr) in enumerate(zip(self.cl_times, self.sr_times)):
            # print ('i: ', i, 'cl: ', cl, 'now_tz: ', self.now_tz, 'sr: ',sr)
            if (cl < self.now_tz < sr):
                if self.now_tz.isoweekday() in (5,6): # It's Friday evening or Saturday before dawn if got here, don't light.
                    return False # shabbos after candlelighting time, so wait for Saturday evening lighting time
                else:
                    print ('light ', i+1, ' candles now') # Still need to queue up next evening's candles
                    return True
        
    def is_waiting_for_lighting_time(self): # It's after a sunrise but before candlighting time.  Find that time. Already corrected for shabbos
        for i, cltime in enumerate(self.cl_times):
            if cltime > self.now_tz:
                return (i+1, cltime)

    def when_to_light_next(self):
        # before first candlelighting time?
        if self.is_now_before_first_candle():
            print ('pause until ', self.cl_times[0])
            return self.cl_times[0]
        elif self.is_now_after_last_sunrise():
            print ('generate next year\'s lighting times; pause until then')
            return self.cl_times[0] # need to fix this one
        elif self.is_during_lighting_time():
            print ('light ', 111, 'candles now')
            return self.now_tz # need to fix this one
        else:
            return self.now_tz # need to fix this one
        
        
    
    
if __name__ == '__main__':
    men = Menorah()
    print ('state: ', men.start)
    # this is how to do a comparison:
    print ('it\'s before the holiday: ', men.start == men.starting_time.BEFORE_HOLIDAY)
    # get timing right:
    print ('\ncurrent_time_utc: \t', men.current_time_utc)
    print ('current time local: \t', men.now_tz)
    print ('before holiday? ', men.is_now_before_first_candle())
    print ('after last candle sunrise? ', men.is_now_after_last_sunrise())
    print ('during a lighting time now? ', men.is_during_lighting_time())
    print ('waiting to light candles? ', men.is_waiting_for_lighting_time())
    print ('candles: ', men.when_to_light_next())