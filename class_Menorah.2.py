"""
class Menorah
Entry point for program.
Finds time and position plus time zone.
Obtains vector of candlelighting times and of corresponding sunrises.
Checks state of holiday at starting time per starting_time enum.
Manages schedule for next candlelighting.
Started 18 December 2025
v.2    20 December 2025
       TODO:
DK
"""


from datetime import datetime, timedelta
from class_hannuka_calendar import hannuka_calendar



class Menorah:
    
    def __init__(self):
        self.current_time_utc = datetime.now()
        self.hc = hannuka_calendar()
        self.cl_times = self.hc.get_candlighting_times()
        self.sr_times = self.hc.get_sunrises()
        self.now_tz =   self.hc.get_now()  # timezone-aware time when object instantiated at plugin
        
    def is_now_before_first_candle(self):  # plugged in menorah before holiday began, True or False
        
        return self.now_tz < self.cl_times[0]
    
    
    def is_now_after_last_sunrise(self):   # plugged in during holiday but after last possible candlelighting, True or False
                                           # will need to create next year's candlelighting times and wait
        return self.now_tz > self.sr_times[7]
    
    
    def is_during_lighting_time(self): # plugged in after a candlighting time but before sunrise, True or False (light now)
        
        for i, (cl, sr) in enumerate(zip(self.cl_times, self.sr_times)):
            if (cl < self.now_tz < sr):    # within period sunset to sunrise, normally light but check for shabbos:
                if self.now_tz.isoweekday() in (5,6): # It's Friday evening or Saturday before dawn if got here, don't light.
                    return False # shabbos after candlelighting time, so wait for Saturday evening lighting time
                else:
                    print ('light ', i+1, ' candles now') # Still need to queue up next evening's candles
                    return True
            else:
                return False # not in a candlelighting time, wait for next one.
        
    def is_waiting_for_lighting_time(self): # It's after a sunrise but before candlighting time.  Find that time.
                                            # (Already corrected for shabbos)
        for i, cltime in enumerate(self.cl_times):
            if cltime > self.now_tz:
                return (i+1, cltime) #(need to unpack to use the datetime object cltime)
            

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
    # get timing right:
    print ('current date/time local: \t', men.now_tz)
    
    # check the span of possibilities on startup for whether to light immediately or to wait:
    print ('before holiday?\t\t\t', men.is_now_before_first_candle())
    print ('after last candle sunrise?\t', men.is_now_after_last_sunrise())
    print ('during a lighting time now?\t', men.is_during_lighting_time())
    print ('light next candles\t\t', men.is_waiting_for_lighting_time()[1])
    print ('candles to light:\t\t', men.is_waiting_for_lighting_time()[0])