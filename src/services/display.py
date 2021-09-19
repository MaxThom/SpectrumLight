import constants as constants
from rpi_ws281x import Color, PixelStrip, ws

class Display():
    def __init__(self):
        self.set_factory_strip_config()

    def __initialize_strip(self):
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
        if "LED_WIDTH" in args and args["LED_WIDTH"]:
            self.strip_config["LED_WIDTH"] = args["LED_WIDTH"]
        if "LED_HEIGHT" in args and args["LED_HEIGHT"]:
            self.strip_config["LED_HEIGHT"] = args["LED_HEIGHT"]
        if "LED_LAYOUT" in args and args["LED_LAYOUT"]:
            self.strip_config["LED_LAYOUT"] = args["LED_LAYOUT"]

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

    def get_pixels_color(self):
        return self.strip.getPixels()

    def get_pixels_color(self, index):
        return self.strip.getPixelColor(index)

    def get_pixels_color_rgbw(self, index):
        if self.strip_config["LED_STRIP"] == ws.SK6812W_STRIP:
            return self.strip.getPixelColorRGBW(index)
        return self.strip.getPixelColorRGB(index)

    def send_frame(self, index, next_frame):        
        try:
            if self.strip_config["LED_LAYOUT"] == 0:
                self.__display_frame_1d(index, next_frame)
            elif self.strip_config["LED_LAYOUT"] == 1:
                self.__display_frame_2d_up_north_snake(index, next_frame)
        except Exception as e: 
            print("Unkown error: " + e)
    
    def __display_frame_1d(self, index, frame):
        for i, led in enumerate(frame):
            if led != None:
                if len(led) == 4:
                    self.strip.setPixelColor(i+index, Color(led[0], led[1], led[2], led[3]))
                else:    
                    self.strip.setPixelColor(i+index, Color(led[0], led[1], led[2], 0))
        self.strip.show()
    
    def __display_frame_2d_up_north_snake(self, index, frame):
        #self.__display_frame_1d(0, [(0,0,0)] * len(frame))
        #frame = [(0,0,100)] * len(frame)

        k = 0
        for i in range(0, len(frame)-16, 16):
            for j in range(0, 16, 1):                
                tile = 16 * 16 * k
                row = 16 * (15 - (i%768)//48)
                index = 0

                if i//768 % 2 == 1:
                    if ((15 - i//48) % 2) == 0:
                        index = tile + row + (15 - j)
                    else:
                        index = tile + row + j
                else:
                    if ((15 - i//48) % 2) == 1:
                        index = tile + row + (15 - j)
                    else:
                        index = tile + row + j
                
                #print(i, j, tile, row)
                #print(index)
                self.strip.setPixelColor((i//768*768)+index, Color(frame[i+j][0], frame[i+j][1], frame[i+j][2]))
                #self.strip.show()
            k = k + 1
            if k == 3:
                k = 0
        self.strip.show()