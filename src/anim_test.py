from rpi_ws281x import Color, PixelStrip, ws
import time
from threading import Thread
import random

# LED strip configuration:
LED_COUNT = 768        # Number of LED pixels.
LED_PIN = 18           # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000   # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10           # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 20    # Set to 0 for darkest and 255 for brightest
LED_INVERT = False     # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0
##LED_STRIP = ws.SK6812_STRIP_RGBW
#LED_STRIP = ws.SK6812W_STRIP
LED_STRIP = ws.WS2812_STRIP

LED_2_COUNT = 768       # Number of LED pixels.
LED_2_PIN = 13          # GPIO pin connected to the pixels (must support PWM! GPIO 13 or 18 on RPi 3).
LED_2_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_2_DMA = 10          # DMA channel to use for generating signal (Between 1 and 14)
LED_2_BRIGHTNESS = 20   # Set to 0 for darkest and 255 for brightest
LED_2_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_2_CHANNEL = 1       # 0 or 1
LED_2_STRIP = ws.WS2812_STRIP

LED_3_COUNT = 768       # Number of LED pixels.
LED_3_PIN = 21          # GPIO pin connected to the pixels (must support PWM! GPIO 13 or 18 on RPi 3).
LED_3_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_3_DMA = 10          # DMA channel to use for generating signal (Between 1 and 14)
LED_3_BRIGHTNESS = 20   # Set to 0 for darkest and 255 for brightest
LED_3_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_3_CHANNEL = 0       # 0 or 1
LED_3_STRIP = ws.WS2812_STRIP


def init_animation():
    print('> Starting LED animation...')
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    strip2 = PixelStrip(LED_2_COUNT, LED_2_PIN, LED_2_FREQ_HZ, LED_2_DMA, LED_2_INVERT, LED_2_BRIGHTNESS, LED_2_CHANNEL, LED_2_STRIP)
    strip3 = PixelStrip(LED_3_COUNT, LED_3_PIN, LED_3_FREQ_HZ, LED_3_DMA, LED_3_INVERT, LED_3_BRIGHTNESS, LED_3_CHANNEL, LED_3_STRIP)
    strip.begin()
    strip2.begin()
    strip3.begin()
    
    #color_wipe_ms_triple(strip, strip2, strip3)
    #color_wipe_ms(strip, strip2, strip3)
    color_blink_ms(strip, strip2, strip3)

    #th_strip1 = Thread(target=color_wipe_infinite, args=(strip, Color(0, 255, 0)))
    #th_strip2 = Thread(target=color_wipe_infinite, args=(strip2, Color(0, 0, 255)))
    #th_strip3 = Thread(target=color_wipe_infinite, args=(strip3, Color(255, 0, 0)))
    #th_strip1.start()
    #th_strip2.start()
    #th_strip3.start()

    #while True:
    #    color_wipe(strip, Color(255, 0, 0))  # Red wipe
    #    color_wipe(strip2, Color(0, 255, 0))  # Gree wipe
    #  #color_wipe(strip, Color(0, 0, 255))  # Blue wipe
    #   
    #   #color_wipe(strip, Color(0, 0, 0, 255))  # White wipe
 
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
        #start = time.time()
        strip.show()
        #end = time.time()
        #print(f"{(end - start) * 1000} ms")
        #time.sleep(wait_ms / 1000.0)

def color_wipe_infinite(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    
    while True:
        color_clear(strip)
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
            #start = time.time()
            strip.show()
            #end = time.time()
            #print(f"{(end - start) * 1000} ms")
            #time.sleep(wait_ms / 1000.0)

def color_wipe_ms_triple(strip1, strip2, strip3):    
    while True:
        color_clear(strip1)
        color_clear(strip2)
        color_clear(strip3)
        for i in range(0, strip1.numPixels(), 3):
            strip1.setPixelColor(i, Color(255, 0, 0))
            strip2.setPixelColor(i+1, Color(0, 255, 0))
            strip3.setPixelColor(i+2, Color(0, 0, 255))
            strip1.show()
            strip2.show()
            strip3.show()

def color_wipe_ms(strip1, strip2, strip3):    
    while True:
        color_clear(strip1)
        color_clear(strip2)
        color_clear(strip3)
        for i in range(strip1.numPixels()):
            strip1.setPixelColor(i, Color(255, 0, 0))
            strip2.setPixelColor(i, Color(0, 255, 0))
            strip3.setPixelColor(i, Color(0, 0, 255))
            start = time.time()
            strip1.show()
            print(f"1: {(time.time() - start) * 1000} ms")
            strip2.show()
            print(f"2: {(time.time() - start) * 1000} ms")
            strip3.show()
            print(f"3: {(time.time() - start) * 1000} ms")

def color_blink_ms(strip1, strip2, strip3):    
    while True:
        color_clear(strip1)
        color_clear(strip2)
        color_clear(strip3)
        for i in range(strip1.numPixels()):
            strip1.setPixelColor(i, Color(255, 0, 0))
            strip2.setPixelColor(i, Color(0, 255, 0))
            strip3.setPixelColor(i, Color(0, 0, 255))
        #start = time.time()
        #strip1.show()
        #print(f"1: {(time.time() - start) * 1000} ms")
        #strip2.show()
        #print(f"2: {(time.time() - start) * 1000} ms")
        #strip3.show()
        #print(f"3: {(time.time() - start) * 1000} ms")

        th_strip1 = Thread(target=strip1.show()) #, args=(strip, Color(0, 255, 0))
        th_strip2 = Thread(target=strip2.show()) #, args=(strip, Color(0, 255, 0))
        th_strip3 = Thread(target=strip3.show()) #, args=(strip, Color(0, 255, 0))
        th_strip1.start()
        th_strip2.start()
        th_strip3.start()
        th_strip1.join()
        th_strip2.join()
        th_strip3.join()


        time.sleep(100/1000)



def color_clear(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

def luka_animation(strip):
    strip.setPixelColor(0, Color(170, 0, 170, 0))
    strip.setPixelColor(1, Color(170, 0, 170, 0))
    strip.setPixelColor(2, Color(170, 0, 170, 0))

    strip.setPixelColor(4, Color(0, 50, 75, 0))
    strip.setPixelColor(5, Color(130, 25, 70, 0))
    strip.setPixelColor(6, Color(10, 255, 70, 200))

    strip.show()

init_animation()