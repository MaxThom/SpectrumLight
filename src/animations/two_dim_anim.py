import time
import math
import animations.array_utils as utils
from animations.anim import __Anim
from random import *

class TwoDimAnim(__Anim):
    def __init__(self, p_display, p_segment):
        super().__init__(p_display, p_segment)
        self.start_index = p_segment[0]
        self.end_index = p_segment[1]
        self.length = self.end_index - self.start_index + 1

    # Flatten and send frame
    def __send_frame(self, next_frame):
        flatten_frame = next_frame[0]
        if type(next_frame[0][0][0]).__name__ == "list":
            for i, row in enumerate(next_frame[0]):
                for j, column in enumerate(row):
                    for k, dim in enumerate(next_frame):
                        if next_frame[k][i][j] != None:
                            flatten_frame[i][j] = next_frame[k][i][j]
                            break
        else:            
            flatten_frame = next_frame

        frame = flatten_frame.flatten()
        self.display.send_frame(self.start_index, frame)

    def __clear(self):
        self.__send_frame(utils.get_colorless_array_1d(self.length))

    def off(self, args):
        self.__clear()

    #
    # Args: color, wait_ms, reverse
    #
    def test(self, args):
        frame = utils.get_colorless_array_2d(48, 48)
        frame[0][5] = (255, 0, 0)
        frame[47][5] = (255, 0, 0)
        frame[47][10] = (255, 0, 0)
        frame[47][15] = (255, 0, 0)
        frame[47][20] = (255, 0, 0)
        frame[47][25] = (255, 0, 0)
        frame[47][30] = (255, 0, 0)
        frame[47][35] = (255, 0, 0)
        frame[47][40] = (255, 0, 0)
        frame[47][45] = (255, 0, 0)
        self.__send_frame(frame)

    #
    # Args: color, wait_ms, reverse
    #
    def color_full(self, args):
        color = utils.array_to_tuple(args["color"]) if "color" in args else (255,255,255)
        frame = utils.get_void_array_1d(self.length, color)
        self.__send_frame(frame)

    #
    # Args: color, wait_ms, reverse
    #
    def color_wipe(self, args):
        color = utils.array_to_tuple(args["color"]) if "color" in args else (0,0,255)
        wait_ms = args["wait_ms"] if "wait_ms" in args else 0.05
        reverse = args["reverse"] if "reverse" in args else False
        start = 0 if not reverse else self.length-1
        end = -1 if reverse else self.length
        step = 1 if not reverse else -1
        
        """Wipe color across display a pixel at a time."""
        while True:
            self.__clear()
            for i in range(start, end, step):
                frame = utils.get_void_array_1d(self.length)
                frame[i] = color
            
                self.__send_frame(frame)
                if (self.isCancelled):
                    return
                time.sleep(wait_ms)

    

    def __wheel(self, pos):
        if pos < 85:
            return (pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return (255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return (0, pos * 3, 255 - pos * 3)
    
    def __get_mouvement_factor(self, x):
        period = 100 # The higher the slower
        cycles = x / period
        tau = math.pi * 2
        raw_sin_wave = math.sin(cycles*tau)
        mouvement_factor = raw_sin_wave / 2 + 0.5
        return mouvement_factor