import time 
from threading import Thread
from queue import PriorityQueue
import constants as constants
from rpi_ws281x import Color, PixelStrip, ws

class OneDimDisplay:
    def __init__(self):
        self.set_factory_strip_config()         
    
    def __del__(self):
        print("Goodbye one dimension !")

    def __initialize_strip(self):
        self.strip = PixelStrip(self.strip_config["LED_COUNT"],
                                self.strip_config["LED_PIN"],
                                self.strip_config["LED_FREQ_HZ"],
                                self.strip_config["LED_DMA"],
                                self.strip_config["LED_INVERT"],
                                self.strip_config["LED_BRIGHTNESS"],
                                self.strip_config["LED_CHANNEL"],
                                self.strip_config["LED_STRIP"],)
        self.strip.begin()

    def set_factory_strip_config(self):
        self.strip_config = {
            "LED_COUNT": constants.LED_COUNT,
            "LED_PIN": constants.LED_PIN,
            "LED_FREQ_HZ": constants.LED_FREQ_HZ,
            "LED_DMA": constants.LED_DMA,
            "LED_INVERT": constants.LED_INVERT,
            "LED_BRIGHTNESS": constants.LED_BRIGHTNESS,
            "LED_CHANNEL": constants.LED_CHANNEL,
            "LED_STRIP": constants.LED_STRIP,
        }
        self.__initialize_strip()

    def set_strip_config(self, args):
        if "LED_COUNT" in args and args["LED_COUNT"]:            
            self.strip_config["LED_COUNT"] = args["LED_COUNT"]
        if "LED_PIN" in args and args["LED_PIN"]:
            self.strip_config["LED_PIN"] = args["LED_PIN"]
        if "LED_FREQ_HZ" in args and args["LED_FREQ_HZ"]:
            self.strip_config["LED_FREQ_HZ"] = args["LED_FREQ_HZ"]
        if "LED_DMA" in args and args["LED_DMA"]:
            self.strip_config["LED_DMA"] = args["LED_DMA"]
        if "LED_INVERT" in args and args["LED_INVERT"]:
            self.strip_config["LED_INVERT"] = args["LED_INVERT"]
        if "LED_BRIGHTNESS" in args and args["LED_BRIGHTNESS"]:
            self.strip_config["LED_BRIGHTNESS"] = args["LED_BRIGHTNESS"]
        if "LED_CHANNEL" in args and args["LED_CHANNEL"]:
            self.strip_config["LED_CHANNEL"] = args["LED_CHANNEL"]
        if "LED_STRIP" in args and args["LED_STRIP"]:
            self.strip_config["LED_STRIP"] = args["LED_STRIP"]

        self.__initialize_strip()

    def get_strip_config(self):
        return self.strip_config

    def get_num_pixels(self):
        return self.strip.numPixels()

    def get_brightness(self):
        return self.strip.getBrightness()

    def set_brightness(self, brightness):
        self.strip_config["LED_BRIGHTNESS"] = brightness
        self.strip.setBrightness(brightness)

    def get_pixels_color(self):
        return self.strip.getPixels()

    def get_pixels_color(self, index):
        return self.strip.getPixelColor(index)

    def get_pixels_color_rgbw(self, index):
        if self.strip_config["LED_STRIP"] == ws.SK6812W_STRIP:
            return self.strip.getPixelColorRGBW(index)
        return self.strip.getPixelColorRGB(index)

    # Receive frame
    def send_frame(self, next_frame):        
        try:
            self.__process_frame(next_frame)
        except Exception as e: 
            print("Unkown error: " + e)

    def __process_frame(self, next_frame):
        frame = [None] * len(next_frame)
        for i, row in enumerate(next_frame):
            if type(row).__name__ == 'tuple' or type(row).__name__ == 'NoneType':
                frame[i] = row
            else:
                for j, column in enumerate(row):
                    if column != None or j == len(row)-1:
                        frame[i] = column
                        break
        self.__display_frame(frame)
    
    def __display_frame(self, frame):
        for i, led in enumerate(frame):
            if led != None:
                if len(led) == 4:
                    self.strip.setPixelColor(i, Color(led[0], led[1], led[2], led[3]))
                else:    
                    self.strip.setPixelColor(i, Color(led[0], led[1], led[2], 0))
        self.strip.show()