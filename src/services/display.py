import constants as constants
from rpi_ws281x import Color, PixelStrip, ws
import time
from threading import Thread
import json
import os.path

class Display():
    def __init__(self):        
        self.CancelRefresh = False
        self.refreshThread = None
        self.anim_mutexes = []

        if os.path.isfile(constants.LED_CONFIG_FILE_PATH):
            # load
            self.__read_config_file()
            self.__initialize_strip()
            print("Setting configurations from file:")
            print(json.dumps(self.strip_config, indent=4))
        else:
            self.set_factory_strip_config()
            print("Setting configurations from default:")
            print(json.dumps(self.strip_config, indent=4))

    def __initialize_strip(self):
        if self.refreshThread != None:
            self.CancelRefresh = True
            self.refreshThread.join()
            self.CancelRefresh = False
        try:
            if self.strip_config["LED_LAYOUT"] == 1:
                self.strip_config["LED_COUNT"] = self.strip_config["LED_WIDTH"] * self.strip_config["LED_HEIGHT"]
            
            self.strip = PixelStrip(self.strip_config["LED_COUNT"],
                                    self.strip_config["LED_PIN"],
                                    self.strip_config["LED_FREQ_HZ"],
                                    self.strip_config["LED_DMA"],
                                    self.strip_config["LED_INVERT"],
                                    self.strip_config["LED_BRIGHTNESS"],
                                    self.strip_config["LED_CHANNEL"],
                                    self.strip_config["LED_STRIP"])            
            self.strip.begin()
            self.strip.begin()
            self.refreshThread = Thread(target=self.__refresh_strip_frame, args=())
            self.refreshThread.start() 
        except Exception as e: 
                print("Unkown error: " + e)

    def __refresh_strip_frame(self):
        while not self.CancelRefresh:
            for mutex in self.anim_mutexes:
                if mutex.locked():
                    mutex.release()
            time.sleep(0.001)
            #start = time.time()
            self.strip.show()
            #end = time.time()
            #print(f"{(end - start) * 1000} ms")
    
    def __write_config_file(self):
        with open(constants.LED_CONFIG_FILE_PATH, 'w') as fp:
            json.dump(self.strip_config, fp, indent=4)
    
    def __read_config_file(self):
        with open(constants.LED_CONFIG_FILE_PATH) as fp:            
            self.strip_config = json.load(fp)

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
            "LED_WIDTH": constants.LED_WIDTH,
            "LED_HEIGHT": constants.LED_HEIGHT,
            "LED_LAYOUT": constants.LED_LAYOUT
        }

        self.__write_config_file()
        self.__initialize_strip()

    def set_strip_config(self, args):
        if "LED_COUNT" in args:            
            self.strip_config["LED_COUNT"] = args["LED_COUNT"]
        if "LED_PIN" in args:
            self.strip_config["LED_PIN"] = args["LED_PIN"]
        if "LED_FREQ_HZ" in args:
            self.strip_config["LED_FREQ_HZ"] = args["LED_FREQ_HZ"]
        if "LED_DMA" in args:
            self.strip_config["LED_DMA"] = args["LED_DMA"]
        if "LED_INVERT" in args:
            self.strip_config["LED_INVERT"] = args["LED_INVERT"]
        if "LED_BRIGHTNESS" in args:
            self.strip_config["LED_BRIGHTNESS"] = args["LED_BRIGHTNESS"]
        if "LED_CHANNEL" in args:
            self.strip_config["LED_CHANNEL"] = args["LED_CHANNEL"]
        if "LED_STRIP" in args:
            self.strip_config["LED_STRIP"] = args["LED_STRIP"]
        if "LED_WIDTH" in args:
            self.strip_config["LED_WIDTH"] = args["LED_WIDTH"]
        if "LED_HEIGHT" in args:
            self.strip_config["LED_HEIGHT"] = args["LED_HEIGHT"]
        if "LED_LAYOUT" in args:
            self.strip_config["LED_LAYOUT"] = args["LED_LAYOUT"]
        
        self.__write_config_file()
        self.__initialize_strip()

    def get_strip_config(self):
        return self.strip_config

    def get_num_pixels(self):
        return self.strip.numPixels()

    def get_num_pixels_2d(self):
        return (self.strip_config["LED_WIDTH"],  self.strip_config["LED_HEIGHT"])

    def get_strip_layout(self):
        return self.strip_config["LED_LAYOUT"]

    def get_brightness(self):
        return self.strip.getBrightness()

    def set_brightness(self, brightness):
        self.strip_config["LED_BRIGHTNESS"] = brightness
        self.strip.setBrightness(brightness)

    def get_pixels_color_all(self):
        return self.strip.getPixels()

    def get_pixels_color(self, index):
        return self.strip.getPixelColor(index)

    def get_pixels_color_rgbw(self, index):
        if self.strip_config["LED_STRIP"] == ws.SK6812W_STRIP:
            return self.strip.getPixelColorRGBW(index)
        return self.strip.getPixelColorRGB(index)

    def send_frame(self, next_frame):        
        try:
            if self.strip_config["LED_LAYOUT"] == 0:
                self.__display_frame_1d(next_frame)
            elif self.strip_config["LED_LAYOUT"] == 1:
                self.__display_frame_2d_up_north_snake(next_frame)
        except Exception as e: 
            print("Unkown error: " + e)
    
    def __display_frame_1d(self, frame):
        for i, led in enumerate(frame):
            if led != None:
                if len(led) == 4:
                    self.strip.setPixelColor(i, Color(led[0], led[1], led[2], led[3]))
                else:    
                    self.strip.setPixelColor(i, Color(led[0], led[1], led[2], 0))
        #self.strip.show()
    
    def __display_frame_2d_up_north_snake(self, frame):
        PANEL_HEIGHT = 16
        PANEL_WIDTH = 16
        PANEL_LEDS = PANEL_WIDTH * PANEL_HEIGHT
        NB_PANEL_PER_ROW = 3
        NB_LEDS_PER_ROW = NB_PANEL_PER_ROW * PANEL_LEDS
        NB_ROWS_PER_ROW = PANEL_HEIGHT * NB_PANEL_PER_ROW

        k = 0
        for i in range(0, len(frame)-PANEL_WIDTH+1, PANEL_WIDTH):
            for j in range(0, PANEL_WIDTH, 1):                
                tile = PANEL_LEDS * k
                row = PANEL_WIDTH * (PANEL_WIDTH-1 - (i%NB_LEDS_PER_ROW)//NB_ROWS_PER_ROW)
                index = 0

                if ((PANEL_WIDTH-1 - i//NB_ROWS_PER_ROW) % 2) == 1:
                    index = tile + row + (PANEL_WIDTH-1 - j)
                else:
                    index = tile + row + j

                if frame[i+j] != None:
                    self.strip.setPixelColor((i//NB_LEDS_PER_ROW*NB_LEDS_PER_ROW)+index, Color(frame[i+j][0], frame[i+j][1], frame[i+j][2]))
                
            k = k + 1
            if k == 3:
                k = 0
        #print("show")
        #self.strip.show()