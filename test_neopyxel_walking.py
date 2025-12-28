import time
import board
import neopixel

NUM_LEDS = 80
pixels = neopixel.NeoPixel(
    board.D18,
    NUM_LEDS,
    brightness=0.3,
    auto_write=False,
    pixel_order=neopixel.GRB
)

# # Light only the LAST LED
# pixels.fill((0,0,0))
# pixels[-1] = (0,255,0)
# pixels.show()
# 
# exit()

# HARD RESET
pixels.fill((0, 0, 0))
pixels.show()
time.sleep(1)

# Walking pixel
for i in range(NUM_LEDS):
    pixels.fill((0, 0, 0))
    pixels[i] = (55, 0, 0)
    pixels.show()
    time.sleep(0.2)

# Final clear
pixels.fill((0, 0, 0))
pixels.show()
