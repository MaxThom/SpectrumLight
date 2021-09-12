  
import time
import math
import animations.array_utils as utils
from rpi_ws281x import Color, PixelStrip, ws
from random import *

class OneDimAnim:
    def __init__(self, p_strip, p_q_frame, p_isCancelled, p_start_index, p_end_index):
        self.strip = p_strip
        self.q_frame = p_q_frame
        self.isCancelled = p_isCancelled
        self.start_index = p_start_index
        self.end_index = p_end_index
        self.length = p_end_index - p_start_index

    def clear(self):
        self.__send_frame(utils.get_colorless_array(self.length))

    def color_wipe(self, color, wait_ms=50):
        print(self)
        print(color, wait_ms)
        """Wipe color across display a pixel at a time."""
        while True:
            self.clear()
            for i in range(self.length):
                frame = utils.get_void_array(self.length)
                frame[i] = color
            # print(frame)
                self.__send_frame(frame)
                if (self.isCancelled()):
                    return
                time.sleep(50 / 1000.0)
    
    def __send_frame(self, frame):
        full_frame = [None] * (self.start_index) + frame + [None] * (self.strip.numPixels() - self.end_index)
        #print(full_frame)
        self.q_frame.put(full_frame)