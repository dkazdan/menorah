import time
import board
import neopixel

NUM_LEDS = 80   # set higher than you think you have
PIN = board.D21

pixels = neopixel.NeoPixel(
    PIN,
    NUM_LEDS,
    brightness=0.1,
    auto_write=False,
    pixel_order=neopixel.RGB
)

pixels.fill((0, 0, 0))
pixels.show()
time.sleep(1)


# --- Test 1: walking pixel ---
print("Walking pixel test")
pixels.fill((0, 0, 0))
pixels.show()

for i in range(NUM_LEDS):
    pixels.fill((0, 0, 0))
    pixels[i] = (255, 0, 0)
    pixels.show()
    time.sleep(0.2)

time.sleep(1)

# --- Test 2: count-up fill ---
print("Count-up fill test")
pixels.fill((0, 0, 0))
pixels.show()

for i in range(NUM_LEDS):
    pixels[i] = (0, 0, 255)
    pixels.show()
    time.sleep(0.1)

time.sleep(1)

# --- Test 3: full white ---
print("Full white test")
pixels.fill((255, 255, 255))
pixels.show()
time.sleep(2)

pixels.fill((0, 0, 0))
pixels.show()

print("Test complete")
