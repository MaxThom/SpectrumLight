from rpi_ws281x import Color, PixelStrip, ws
import time
from threading import Thread
import random
from PIL import Image
import numpy as np
#from scipy import misc

# LED strip configuration:
LED_COUNT = 2304        # Number of LED pixels.
LED_PIN = 18           # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000   # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10           # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 20    # Set to 0 for darkest and 255 for brightest
LED_INVERT = False     # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0
##LED_STRIP = ws.SK6812_STRIP_RGBW
#LED_STRIP = ws.SK6812W_STRIP
LED_STRIP = ws.WS2812_STRIP

def init_animation():
    print('> Starting LED animation...')
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    strip.begin()
    get_image_rgb_array()
    color_clear(strip)
    while True:
        color_wipe(strip, Color(255, 0, 0))  # Red wipe
        color_wipe(strip, Color(0, 255, 0))  # Gree wipe
        color_wipe(strip, Color(0, 0, 255))  # Blue wipe
       
       #color_wipe(strip, Color(0, 0, 0, 255))  # White wipe

def get_image_rgb_array():
    im = np.array(Image.open('../anim_frames/anim_test.bmp'))
    #im = np.array(im.tolist())
    print(im)
    print(np.shape(im))
    print(im.dtype)
    #new_im = im.view(dtype=np.dtype([('x', im.dtype), ('y', im.dtype)]))
    #new_im = new_im.reshape(new_im.shape[:-1])
    #print(new_im)
    x = np.empty((im.shape[0], im.shape[1]), dtype=tuple)
    #x.fill(init_value)
    for ix,iy,iz in np.ndindex(im.shape):
        x[ix,iy] = tuple(im[ix,iy])
        print(tuple(im[ix,iy]))
    print(x)
    #arr = misc.imread('../anim_frames/anim_test.bmp') # 640x480x3 array
    #print(arr)
    #printt(np.shape(arr))


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
        #for i in range(1, strip1.numPixels(), 3):
        #    strip1.setPixelColor(i, Color(0, 255, 0))
        #    strip2.setPixelColor(i+1, Color(0, 0, 255))
        #    strip3.setPixelColor(i+2, Color(255, 0, 0))
        #    strip1.show()
        #    strip2.show()
        #    strip3.show()
        #for i in range(2, strip1.numPixels(), 3):
        #    strip1.setPixelColor(i, Color(0, 0, 255))
        #    strip2.setPixelColor(i+1, Color(255, 0, 0))
        #    strip3.setPixelColor(i+2, Color(0, 255, 0))
        #    strip1.show()
        #    strip2.show()
        #    strip3.show()

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