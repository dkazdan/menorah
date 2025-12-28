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
DK
"""

# https://docs.circuitpython.org/projects/neopixel/en/latest/api.html
import board, neopixel, random
import time # need monotonic, sleep

NUM_SEGMENTS = 9
LEDS_PER_SEGMENT = 8
NUM_LEDS = NUM_SEGMENTS * LEDS_PER_SEGMENT

pixels = neopixel.NeoPixel(
    board.D18,           # GPIO pin; 18 is the usual one for 2812a LED strings
    NUM_LEDS,
    brightness=0.3,
    auto_write=False,
    pixel_order=neopixel.GRB
)

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.

class Menorah:
    def __init__(self, pixels, start=0, candles=9, leds_per_candle=8):
        self.pixels = pixels
        self.candles = []

        for i in range(candles):
            seg_start = start + i * leds_per_candle
            candle = self.CandleSegment(
                pixels=pixels,
                start=seg_start,
                length=leds_per_candle,
                burn_minutes=30
            )
            self.candles.append(candle)

    def update(self, now):
        for candle in self.candles:
            candle.update(now)

    def relight_all(self):
        for candle in self.candles:
            candle.start_time = time.monotonic()
            candle.burned_out = False

    def clear(self):
        for candle in self.candles:
            candle._clear()


    class CandleSegment:
        def __init__(self, pixels, start, length,
                     burn_minutes=30,
                     wax_color=(255, 120, 40)):
            self.pixels = pixels
            self.start = start
            self.length = length

            # burn timing
            base = burn_minutes * 60
            self.burn_duration = base * random.uniform(0.9, 1.1)
            self.start_time = time.monotonic()

            # visual
            self.wax_color = wax_color
            self.flame_color = (255, 180, 40)

            # flicker state
            self.next_flicker = self.start_time
            self.flame_scale = 1.0

            self.burned_out = False

        def update(self, now):
            if self.burned_out:
                self._clear()
                return

            elapsed = now - self.start_time
            progress = min(elapsed / self.burn_duration, 1.0)

            # remaining height
            remaining = int(self.length * (1.0 - progress))

            if remaining <= 0:
                self.burned_out = True
                self._clear()
                return

            # draw wax
            for i in range(self.length):
                idx = self.start + i
                if i < remaining - 1:
                    self.pixels[idx] = self.wax_color
                else:
                    self.pixels[idx] = (0, 0, 0)

            # flame flicker
            if now >= self.next_flicker:
                self.flame_scale = random.uniform(0.7, 1.2)
                self.next_flicker = now + random.uniform(0.03, 0.12)

            flame_idx = self.start + remaining - 1
            self.pixels[flame_idx] = self._scale_color(
                self.flame_color, self.flame_scale
            )

        def _scale_color(self, color, scale):
            return tuple(min(255, int(c * scale)) for c in color)

        def _clear(self):
            for i in range(self.start, self.start + self.length):
                self.pixels[i] = (0, 0, 0)


if __name__ == "__main__":
# pixels created ONCE here
    menorah = Menorah(pixels)

    while True:
        now = time.monotonic()
        menorah.update(now)
        pixels.show()
        time.sleep(0.02)
    
