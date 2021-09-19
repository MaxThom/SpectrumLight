from rpi_ws281x import Color, PixelStrip, ws
import time 
import random

# LED strip configuration:
LED_COUNT = 650        # Number of LED pixels.
LED_PIN = 18           # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000   # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10           # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 20   # Set to 0 for darkest and 255 for brightest
LED_INVERT = False     # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0
##LED_STRIP = ws.SK6812_STRIP_RGBW
#LED_STRIP = ws.SK6812W_STRIP
LED_STRIP = ws.WS2812_STRIP

def init_animation():
    print('> Starting LED animation...')
    # Create NeoPixel object with appropriate configuration.
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    
    #luka_animation(strip)
    

    while True:
        #color_full(strip)
       # Color wipe animations.
       color_wipe(strip, Color(255, 0, 0))  # Red wipe
       color_wipe(strip, Color(0, 255, 0))  # Gree wipe
       color_wipe(strip, Color(0, 0, 255))  # Blue wipe
       #color_wipe(strip, Color(0, 0, 0, 255))  # White wipe
 
def color_full(strip):
    """Wipe color across display a pixel at a time."""
    color = [None] * 9
    color[0] = Color(random.randint(0,255), random.randint(0,255), random.randint(0,255))
    color[1] = Color(random.randint(0,255), random.randint(0,255), random.randint(0,255))
    color[2] = Color(random.randint(0,255), random.randint(0,255), random.randint(0,255))
    color[3] = Color(random.randint(0,255), random.randint(0,255), random.randint(0,255))
    color[4] = Color(random.randint(0,255), random.randint(0,255), random.randint(0,255))
    color[5] = Color(random.randint(0,255), random.randint(0,255), random.randint(0,255))
    color[6] = Color(random.randint(0,255), random.randint(0,255), random.randint(0,255))
    color[7] = Color(random.randint(0,255), random.randint(0,255), random.randint(0,255))
    color[8] = Color(random.randint(0,255), random.randint(0,255), random.randint(0,255))
    for i in range(0, strip.numPixels(), 256):
        for j in range(i, i+256, 1):
            strip.setPixelColor(j, color[i // 256])
        strip.show()
        

def color_wipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        start = time.time()
        strip.show()
        end = time.time()
        print(f"{(end - start) * 1000} ms")
        #time.sleep(wait_ms / 1000.0)

def luka_animation(strip):
    strip.setPixelColor(0, Color(170, 0, 170, 0))
    strip.setPixelColor(1, Color(170, 0, 170, 0))
    strip.setPixelColor(2, Color(170, 0, 170, 0))

    strip.setPixelColor(4, Color(0, 50, 75, 0))
    strip.setPixelColor(5, Color(130, 25, 70, 0))
    strip.setPixelColor(6, Color(10, 255, 70, 200))

    strip.show()

init_animation()