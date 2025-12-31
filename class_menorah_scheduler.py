"""
Class menorah_scheduler.py
Creates menorah object,
runs its schedule for chanukah
Begun 31 December 2025
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



# def scheduled_job():
#     print("Job ran at", datetime.now())
# 
# # Create the scheduler
# scheduler = BlockingScheduler() # I think this is the correct one to use; might need non-blocking
# 
# # Pick a time to schedule a job
# specific_time = datetime(2025, 12, 31, 15, 48, 0, tzinfo=ZoneInfo("America/New_York"))
# scheduler.add_job(scheduled_job, 'date', run_date=specific_time)#, args=['Job executed once'])
# 
# print("Starting scheduler...")
# # Start the scheduler
# try:
#     scheduler.start()
# except (KeyboardInterrupt, SystemExit):
#     pass


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
        self.hc=hannuka_calendar()
        self.cl_times = self.hc.get_candlighting_times()
        self.sr_times = self.hc.get_sunrises()



# test code
if __name__ == "__main__":

    sched = menorah_scheduler()
# 
#     NIGHT = 3   # i.e., light 3 candles + shamash
#     menorah.set_shabbos(False)
#     print('light menorah')
# 
#     menorah.light_n_candles(NIGHT)
# 
#     try:
#         while True: # loop updates all candles at 50 frames per second
#             now = time.monotonic()
#             menorah.update(now)
#             led_strip.show()
#             time.sleep(0.02)   # 0.02 seconds = 50 FPS
#             if menorah.all_burned_out() == True: # all candles are down to zero length
#                 menorah.clear()
#                 print("candles all burned out")
#                 exit()
#     except KeyboardInterrupt:
#         menorah.clear()
#         led_strip.show()
# 