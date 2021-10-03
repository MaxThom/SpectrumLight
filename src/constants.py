from rpi_ws281x import Color, PixelStrip, ws

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
LED_WIDTH = 48
LED_HEIGHT = 48
LED_LAYOUT = 1 # 0 = 1d, 1 = 2d south_north_snake

# Thread priority
TH_PRIORITY_HIGH = 0.0100
TH_PRIORITY_MEDIUM = 0.0200
TH_PRIORITY_LOW = 0.0300

# Configs
LED_CONFIG_FILE_PATH = "../configs/config"