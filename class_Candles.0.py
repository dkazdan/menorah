"""
MUST RUN FROM ROOT

Class to produce 9 inner classes of Neopixel candles.
Neopixels need to be in a string, only one per Pi,
so will use separate object for each candle.
Use object 0 for shammos,
objects 1-8 for daily hanukkah candles.
Started 12 December 2024
DK
"""

import board
# https://docs.circuitpython.org/projects/neopixel/en/latest/api.html
import neopixel
from time import sleep

num_pixels = 8
pixel_pin = board.D18

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

redspot=0
while(True):
    if redspot == num_pixels:
        redspot = 0
    #pixels.fill(0,255,0)
    pixels.fill((0, 0, 125))
    pixels[redspot] = (255, 0, 0)
    pixels.show()
    sleep(.1)
    redspot += 1

# light all pixels green
pixels.fill((0, 255, 0))
pixels.show()

