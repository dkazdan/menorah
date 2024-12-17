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

import board
# https://docs.circuitpython.org/projects/neopixel/en/latest/api.html
import neopixel
from time import time, sleep
import sched
s = sched.scheduler(time, sleep)
import random

num_pixels = 8
pixel_pin = board.D18

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

class candle:
    def __init__(self,candle_number,n_pixels):
        self.n_pixels = n_pixels
        self.candle_number = candle_number
        
        # set pixels to dim value, show
        self.first_pixel = self.candle_number * self.n_pixels        
        for LED in range(self.first_pixel, self.first_pixel+self.n_pixels):
            pixels[LED] = ((10,10,10))
        pixels.show()
        
    def light_candle(self):
        candle_yellow = 0x996600
        flame_red = (200,0,0)
        for LED in range(self.first_pixel, self.first_pixel+self.n_pixels-1):
            pixels[LED] = (candle_yellow)
        pixels[self.n_pixels -1] = flame_red
        pixels.show()

def burncandle():
    pixels.fill ((0,0,0))
    pixels.show()
    
    candle_yellow = 0x996600
    flame_red = (100,5,5)
    pixels.fill(candle_yellow)
    #pixels[num_pixels-1] = 0x000000
    pixels[num_pixels-1] = flame_red
    pixels.show()
    
    
    last_wax = num_pixels-2
    
    while (last_wax > 0):
        delay = random.gauss(10,.1)
        if delay<0: delay=abs(delay)
        sleep(delay)
        # TODO: Make yellow dimmer toward base of candle
        pixels[last_wax+1] = 0x000000
        # TODO: Put sparkle/twinkle in flame
        pixels[last_wax] = flame_red 
        pixels.show()
        last_wax -= 1
    # and burnout
    delay = random.gauss(2.5,.5)
    if delay<0: delay=abs(delay)
    sleep(delay)
    # TODO: have schedule burn candle down one segment
    pixels[0] = 0x000000
    pixels[1] = 0x000000 
    pixels.show()
    

def lightcandle():
    pixels.fill((0,0,0))
    pixels.show()
    wax_top = num_pixels - 1
    # start with mostly dull yellow wax
    brightness = 50
    color = (int(brightness*.5), int(brightness * 0.35), int(brightness * 0.1))  # Candle color (orange-ish)
    pixels.fill(color)
    # TODO: add randomness to top candles and to burning down.
    pixels[num_pixels-1] = (50,50,50)
    pixels.show()
    sleep(5)
    brightness = random.randint(100, 255)
    color = (brightness, int(brightness * 0.7), int(brightness * 0.2))  # Candle color (orange-ish)
    pixels.fill(color)
    while True:
        pixel_adjust = int(random.triangular(0, num_pixels-1, num_pixels-2)+1)
        adjust = (num_pixels-pixel_adjust)/num_pixels
        brightness = random.randint(int(50*adjust), int(255*adjust))
        #color = (int(brightness*.5), int(brightness * 0.35), int(brightness * 0.1))  # Candle color (orange-ish)
        color = (int(brightness*.5 * (1.-adjust/2)),
                 int(brightness * 0.35 * adjust),
                 int(brightness * adjust))  # Candle color (orange-ish)
        pixels[pixel_adjust] = color
        pixels.show()
        
        sleep(random.uniform(0.01, 0.05)) # random flicker delay


if __name__ == "__main__":
    try:
        candle0 = candle(0,8)
        candle0.light_candle()
        
        #burncandle()
        #lightcandle()
    except KeyboardInterrupt:
        pixels.fill((0,0,0))
        pixels.show