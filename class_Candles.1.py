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
import random

num_pixels = 8
pixel_pin = board.D18

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

def lightcandle():
    pixels.fill((0,0,0))
    brightness = random.randint(100, 255)
    color = (brightness, int(brightness * 0.7), int(brightness * 0.2))  # Candle color (orange-ish)
    pixels.fill(color)
    while True:
        pixel_adjust = random.randint(0,num_pixels-1)
        brightness = random.randint(100, 255)
        color = (int(brightness*.5), int(brightness * 0.35), int(brightness * 0.1))  # Candle color (orange-ish)
        pixels[pixel_adjust] = color
        pixels.show()
        
        sleep(random.uniform(0.05, 0.25)) # random flicker delay


if __name__ == "__main__":
    try:
        lightcandle()
    except KeyboardInterrupt:
        pixels.fill((0,0,0))
        pixels.show