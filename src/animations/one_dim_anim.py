import time
import math
import animations.array_utils as utils
from animations.anim import __Anim
from random import *

class OneDimAnim(__Anim):
    def __init__(self, p_display, p_segment):
        super().__init__(p_display, p_segment)
        self.start_index = p_segment[0]
        self.end_index = p_segment[1]
        self.length = self.end_index - self.start_index + 1

    def clear(self, args):
        self._send_frame(utils.get_colorless_array_1d(self.length))

    #
    # Args: color, wait_ms, reverse
    #
    def test(self, args):
        frame = utils.get_void_array_1d(self.length, (0, 0, 255))
        frame = utils.add_void_layer_1d(frame)
        frame[0][5] = (255, 0, 0)
        frame[0][10] = (255, 0, 0)
        frame[0][15] = (255, 0, 0)
        frame[0][20] = (255, 0, 0)
        frame[0][25] = (255, 0, 0)
        frame[0][30] = (255, 0, 0)
        frame[0][35] = (255, 0, 0)
        frame[0][40] = (255, 0, 0)
        frame[0][45] = (255, 0, 0)
        frame[0][50] = (255, 0, 0)
        frame[0][55] = (255, 0, 0)
        frame[0][60] = (255, 0, 0)
        frame[0][65] = (255, 0, 0)
        frame[0][70] = (255, 0, 0)
        frame[0][75] = (255, 0, 0)
        frame = utils.add_void_layer_1d(frame)
        frame[0][5] =  (0, 255, 0)
        frame[0][15] = (0, 255, 0)
        frame[0][25] = (0, 255, 0)
        frame[0][35] = (0, 255, 0)
        frame[0][45] = (0, 255, 0)
        frame[0][55] = (0, 255, 0)
        frame[0][65] = (0, 255, 0)
        frame[0][75] = (0, 255, 0)
        self._send_frame(frame)

    #
    # Args: color, wait_ms, reverse
    #
    def color_wipe(self, args):
        color = utils.array_to_tuple(args["color"])
        wait_ms = args["wait_ms"]
        reverse = args["reverse"]
        start = 0 if not reverse else self.length-1
        end = -1 if reverse else self.length
        step = 1 if not reverse else -1
        
        """Wipe color across display a pixel at a time."""
        while True:
            self.clear(None)
            for i in range(start, end, step):
                frame = utils.get_void_array_1d(self.length)
                frame[i] = color
            
                self._send_frame(frame)
                if (self.isCancelled):
                    return
                time.sleep(wait_ms / 1000.0)
    
    #
    # Args: wait_ms
    #
    def rainbow_cycle(self, args):
        wait_ms = args["wait_ms"]
        self.clear(None)
        while True:
            for j in range(256): # one cycle of all 256 colors in the wheel
                frame = utils.get_void_array_1d(self.length)
                for i in range(self.length):
                    frame[i] = self.wheel(((i * 256 // self.length) + j) % 256)
                if (self.isCancelled):
                    return
                self._send_frame(frame)
                if wait_ms > 0:
                    time.sleep(wait_ms)
                if (self.isCancelled):
                    return
    
    def wheel(self, pos):
        if pos < 85:
            return (pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return (255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return (0, pos * 3, 255 - pos * 3)
    
    