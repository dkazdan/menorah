"""
Class menorah_scheduler.py
Creates menorah object,
runs its schedule for chanukah
Begun 31 December 2025

Use
to get dictionary of source, position, timezone

    pf = position_finder()
    position_dictionary = pf.get_position()

to get tuple of candlelighting times and of sunrise times,
    sched = menorah_scheduler()
    cl_times = sched.get_candlelighting_times()
    sr_times = sched.get_sunrises()

    
DK
"""

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from zoneinfo import ZoneInfo
import time

from class_menorah import Menorah
import neopixel
import board
from class_hannuka_calendar import hannuka_calendar
from class_position_finder import position_finder

class menorah_scheduler:
    def __init__(self):
        # 1) prepare a menorah
        self.NUM_CANDLES = 9
        self.LEDS_PER_CANDLE = 8
        self.NUM_LEDS = self.NUM_CANDLES * self.LEDS_PER_CANDLE

        self.led_strip = neopixel.NeoPixel(
            board.D21, # NOTE: Not usual D18
            self.NUM_LEDS,
            brightness=0.3,
            auto_write=False,
            pixel_order=neopixel.GRB
        )
        
        self.menorah = Menorah(self.led_strip)

        # 2) get an initial set of candlelighting times and sunrise times
        pf = position_finder()
        self.position_dictionary = pf.get_position()
        print(self.position_dictionary)
        self.hc=hannuka_calendar()
        self.cl_times = self.hc.get_candlighting_times()
        self.sr_times = self.hc.get_sunrises()
        
    def get_candlelighting_times(self):
        return self.cl_times
    
    def get_sunrises(self):
        return self.sr_times

# test code
if __name__ == "__main__":

    sched = menorah_scheduler()
    cl_times = sched.get_candlelighting_times()
    for sunset in cl_times:
        print (sunset)
    print('\n')
    sr_times = sched.get_sunrises()
    for sunrise in sr_times:
        print(sunrise)