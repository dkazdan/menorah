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
DK
"""

# https://docs.circuitpython.org/projects/neopixel/en/latest/api.html
import board, neopixel, sched, random
from time import time, sleep
s = sched.scheduler(time, sleep)

num_pixels = 8 # on each candle's neopixel strip
pixel_pin = board.D18

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.

class menorah:
    def __init__(self, n_pixels_per_candle=8, n_candles=9): # 1 is shammos only
        ORDER = neopixel.GRB # this actually produces RGB, not sure why
        self.pixels = neopixel.NeoPixel(
            pixel_pin, num_pixels, brightness=0.2, auto_write=True,
            pixel_order=ORDER)

        self.n_pixels = n_pixels_per_candle
        self.candles = n_candles # total number of candles in candelabra
        self.candle_yellow = (100,75,0)
        self.flame_red = (200,0,0)
        Candles=[]
        for i in range (0, n_candles): # 0, 8 covers hanukkah candles 1 through 8 plus shamash
            # print(i)
            Candles.append(self.candle(self, i, n_pixels=8))
        Candles[0].light_candle()


    class candle:
        # sets up indiidual candles in the NeoPixel string. 45 minutes for weekday hanukkah candles; use 90 minutes for shabbos.
        def __init__(self, menorah, candle_number,n_pixels=8, minutes=90):
            self.menorah=menorah
            self.candle_number = candle_number
            self.burning_time = 60 * minutes # burning time in seconds
            self.n_pixels = n_pixels
            self.first_pixel = self.candle_number * self.n_pixels
            self.candle_yellow = (50,35,0)
            self.flame_red = (200,0,0)

        def light_candle(self):
            
            for LED in range(self.first_pixel, self.first_pixel+self.n_pixels-1):
                self.menorah.pixels[LED] = self.candle_yellow
            self.menorah.pixels[self.n_pixels -1] = self.flame_red
            self.burncandle(self.n_pixels-1)
            
        def burncandle(self, last_wax): # highest point of candle
            if (last_wax == 0): # candle is burned to stub
                self.menorah.pixels.fill((0,0,0)) # extinguish candle
                return
            # else
            segment_burning_time = self.burning_time / (self.n_pixels-1)
            burn_time = abs(random.gauss(segment_burning_time, segment_burning_time/10))  # might have negative tail
            sleep(burn_time)
            last_wax -= 1
            self.menorah.pixels[last_wax] = self.flame_red
            self.menorah.pixels[last_wax +1] = ((0,0,0))
            
            self.burncandle(last_wax)


if __name__ == "__main__":

    Menorah = menorah(n_candles=1)
    #candle0.light_candle()
