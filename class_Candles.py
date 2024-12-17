"""
Class to produce 9 inner classes of Neopixel candles.
Neopixels need to be in a string, only one per Pi,
so will use separate object for each candle.
Use object 0 for shammos,
objects 1-8 for daily hanukkah candles.
Started 12 December 2024
DK
"""

import board
import neopixel
pixels = neopixel.NeoPixel(board.D18, 30)