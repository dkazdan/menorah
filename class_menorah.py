"""
MUST RUN FROM ROOT

Class to produce 9 inner classes of Neopixel candles.
Neopixels need to be in a string, only one per Pi,
so will use separate object for each candle.
Use object 0 for shammos,
objects 1-8 for daily hanukkah candles.
v. 3 runs candles with some color and frequency randomness from top to bottom.
v. 4 better candle demonstration
v. 5 try with sched.scheduler
v. 6 Start writing classes
v. 7 Write candles as inner class to menorah
Started 12 December 2024
v. 8 Restart writing this 20 December 2025 after some ChatGPT queries.
v. 9 Rewritten from v.8 after different query
v. 10 Start implementing some changes ChatGPT suggests such as graceful extinguish and flame sparkle
v. 11 Getting ready to install full 9 candles. Set NUM_CANDLES to 1 in test code.
Resaved as class_menorah.py 29 Dec 2025
30 Dec 2025
Added shamash behavior, candle 0 is marked as shamash and that increases its burn time 50%.
DK
"""

# https://docs.circuitpython.org/projects/neopixel/en/latest/api.html
import time
import random
import math # for ceil

import board
import neopixel

NORMAL_BURN_MINUTES = 30
SHABBOS_BURN_MINUTES = 120


class Menorah:
    class Candle:
        def __init__(self, pixels, start, length, burn_minutes=60, is_shamash=False):
            # pixels is object representing entire LED strip (say, 9 candles x 8 LEDs/candle)
            # start is index of this strip (candle 0 -> index 0, candle 1 -> index 8, candle 2 -> index 16 etc.
            # length is number of LEDs per strip; here, 8.
            # (If an object controls a slice of a shared resource, pass: (resource, start, length))
                        
            self.pixels = pixels # object for entire strip
            self.start = start   # index along strip for this candle
            self.length = length # number of LEDs in this candle
            self.is_shamash = is_shamash # candle [0] should be shamash, has different behavior

            base = burn_minutes * 60  # burn time in seconds without randomizer.
            if self.is_shamash:
                base *= 1.5           # have shamash burn 50% longer than other candles.
            self.burn_duration = base * random.uniform(0.8, 1.2)  # include randomizer; might use Gaussian
            self.start_time = time.monotonic()
            self.burned_out = False

            self.wax_color = (5, 5, 20) # RGB (255, 120, 40) original from ChatGPT
            self.flame_color = (100, 45, 10)

            self.next_flicker = self.start_time
            self.flame_scale = 1.0

        def update(self, now):
            if self.burned_out:
                # self._clear()  # clear already happened when candle burned out
                return
            # else:
            elapsed = now - self.start_time
            progress = min(elapsed / self.burn_duration, 1.0) # fraction of candle burned

            #remaining = int(self.length * (1.0 - progress)) # causing only 7 LEDs to light for rounding error on progress
            remaining = math.ceil(self.length * (1.0 - progress))
            if remaining <= 0:  # no wax left, or "negative wax" left
                self.burned_out = True
                self._clear()
                return

            # wax, set color
            for i in range(self.length): # 0-7 here
                idx = self.start + i  # index: That LED position along the total array
                self.pixels[idx] = self.wax_color if i < remaining - 1 else (0, 0, 0) # extinguish

            # flicker, set colors
            if now >= self.next_flicker: # change flame intensity, compute next flicker time
                self.flame_scale = random.uniform(0.7, 1.2) # change to Gaussian?
                self.next_flicker = now + random.uniform(0.06, 0.18)

            flame_idx = self.start + remaining - 1 # highest-number LED among the remaining
            self.pixels[flame_idx] = self._scale(self.flame_color, self.flame_scale)

        def _scale(self, color, scale): # set new flame tuple
            return tuple(min(255, int(c * scale)) for c in color)

        def _clear(self): # extinguish this candle
            for i in range(self.start, self.start + self.length):
                self.pixels[i] = (0, 0, 0)

        def relight(self):
            self.start_time = time.monotonic()
            self.burned_out = False

    # -------- Menorah itself --------
    # Use a method call to restart the menorah each night
    def __init__(self, strip, candles=9, leds_per_candle=8, shabbos=False):
        self.pixels = strip
        self.candles = []
        self.shabbos = shabbos
        
        burn_minutes = SHABBOS_BURN_MINUTES if shabbos else NORMAL_BURN_MINUTES # defined at top of file

        for i in range(candles):
            start = i * leds_per_candle
            candle = Menorah.Candle(
                pixels=self.pixels,
                start=start,
                length=leds_per_candle,
                burn_minutes=30,
                is_shamash = (i == 0) # candle [0] gets set to shamash behavior
            )
            self.candles.append(candle)
            
    def set_shabbos(self, shabbos: bool):  # Call this method when lighting if day is Friday
        burn_minutes = SHABBOS_BURN_MINUTES if shabbos else NORMAL_BURN_MINUTES

        for candle in self.candles:
            base = burn_minutes * 60 # base amount of time for candle burn, seconds
            if candle.is_shamash:
                base *= 1.5    # shamash should burn longer than mitzvah candles
            candle.burn_duration = base * random.uniform(0.9, 1.1)
            candle.relight()

    def light_n_candles(self, n):
        """
        Light shamash + first n candles.
        n = number of regular candles
        n = 0 will light shamash only
        """
        for i, candle in enumerate(self.candles):
            if candle.is_shamash:
                candle.relight()
            elif 1 <= i <= n:
                candle.relight()
            else:
                candle.burned_out = True


    def update(self, now):
        for candle in self.candles:
            candle.update(now)

    def relight_all(self):
        for candle in self.candles:
            candle.relight()

    def clear(self):
        for candle in self.candles:
            candle._clear()
            
    def all_burned_out(self):
        for candle in self.candles:
            if candle.burned_out == False:
                return False # any one candle still burning means not all burned out
        return True          # if got here, they're all burned out
            
            
"""
Test code
"""

if __name__ == "__main__":
    NUM_CANDLES = 9
    LEDS_PER_CANDLE = 8
    NUM_LEDS = NUM_CANDLES * LEDS_PER_CANDLE

#    pixels = neopixel.NeoPixel(
    led_strip = neopixel.NeoPixel(
        board.D21, # NOTE: Not usual D18
        NUM_LEDS,
        brightness=0.3,
        auto_write=False,
        pixel_order=neopixel.GRB
    )
    
#     # TEST CODE TO START ALL LEDS
#     
#     for i in range(NUM_LEDS):
#         led_strip[i] = (0, 0, 55)
# 
#     led_strip.show()
#     time.sleep(2)


#    menorah = Menorah(pixels)
    menorah = Menorah(led_strip)

    NIGHT = 1   # i.e., light 3 candles + shamash
    menorah.set_shabbos(True)
    menorah.light_n_candles(NIGHT)

    try:
        while True: # loop updates all candles at 50 frames per second
            now = time.monotonic()
            menorah.update(now)
            led_strip.show()
            time.sleep(0.02)   # 0.02 seconds = 50 FPS
            if menorah.all_burned_out() == True: # all candles are down to zero length
                menorah.clear()
                print("candles all burned out")
                exit()
    except KeyboardInterrupt:
        menorah.clear()
        led_strip.show()
