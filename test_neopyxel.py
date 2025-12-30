import time
import board
import neopixel

NUM_LEDS = 80   # set higher than you think you have
PIN = board.D21 # NOTE THIS IS NOT THE USUAL D18

pixels = neopixel.NeoPixel(
    PIN,
    NUM_LEDS,
    brightness=0.1,
    auto_write=False,
    pixel_order=neopixel.RGB # actually produces GRB
)

pixels.fill((0, 0, 0))
pixels.show()
time.sleep(1)


# --- Test 1: walking pixel ---
print("Walking pixel test", flush=True)
pixels.fill((0, 0, 0))
pixels.show()

for i in range(NUM_LEDS):
    pixels.fill((0, 0, 0))
    pixels[i] = (0, 125, 0)
    pixels.show()
    if i < (NUM_LEDS-1):  # don't delay on last light
        time.sleep(0.2)
        
time.sleep(1)

# --- Test 2: count-up fill ---
print("Count-up fill test", flush=True)
pixels.fill((0, 0, 0))
pixels.show()

for i in range(NUM_LEDS):
    pixels[i] = (0, 0, 127)
    pixels.show()
    time.sleep(0.1)

time.sleep(1)

# --- Test 3: full white ---
print("Full white test", flush=True)
pixels.fill((127, 127, 127))  # this takes about 400 microseconds
pixels.show()
time.sleep(2)

pixels.fill((0, 0, 0))
pixels.show()

print("Test complete")
