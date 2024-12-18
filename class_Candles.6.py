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


class candle:
    def __init__(self,candle_number,n_pixels):
        ORDER = neopixel.GRB # this actually produces RGB, not sure why
        self.pixels = neopixel.NeoPixel(
            pixel_pin, num_pixels, brightness=0.2, auto_write=True,
            pixel_order=ORDER)

        self.n_pixels = n_pixels
        self.candle_number = candle_number
        self.candle_yellow = (100,75,0)
        # set pixels to dim value, show
        self.first_pixel = self.candle_number * self.n_pixels

    def light_candle(self):
        
        flame_red = (200,0,0)
        for LED in range(self.first_pixel, self.first_pixel+self.n_pixels-1):
            self.pixels[LED] = (self.candle_yellow)
        self.pixels[self.n_pixels -1] = ((100,0,0))
        self.burncandle(self.n_pixels-1)
        
    def burncandle(self, last_wax):
        if (last_wax == 0):
            self.pixels.fill((0,0,0))
            return
        # else
        burn_time = random.gauss(5,1)
        burn_time=abs(burn_time) # might have negative tail
        sleep(burn_time)
        last_wax -= 1

        candle_yellow = 0x996600
        flame_red = (100,5,5)
        self.pixels[last_wax] = flame_red
        self.pixels[last_wax +1] = ((0,0,0))
        
        self.burncandle(last_wax)


if __name__ == "__main__":
    try:
        candle0 = candle(0,8)
        candle0.light_candle()
        
        #burncandle()
        #lightcandle()
    except KeyboardInterrupt:
        pixels.fill((0,0,0))
        pixels.show()