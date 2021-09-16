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
        color = utils.array_to_tuple(args["color"]) if "color" in args else (0,0,0,255)
        wait_ms = args["wait_ms"] if "wait_ms" in args else 0.05
        reverse = args["reverse"] if "reverse" in args else False
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
        wait_ms = args["wait_ms"] if "wait_ms" in args else 0.05
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

    def labyrinth(self, args):
        # Init arguments
        wait_ms = args["wait_ms"] if "wait_ms" in args else 0.05
        count = args["count"] if "count" in args else 10
        turn_chance = args["turn_chance"] if "turn_chance" in args else 2
        color = utils.array_to_tuple(args["color"]) if "color" in args else (0,0,0,255)
        contact_color = utils.array_to_tuple(args["contact_color"]) if "contact_color" in args else (127, 127, 127, 0)

        self.clear(None)
        points = []
        points_location = {}
        points_contact = {}
        for i in range(count):
            start = randint(0, self.length)
            velocity = randint(0, 1)
            if (velocity == 0):
                velocity = -1
            points.append(utils.Point(start, velocity))

        while (not self.isCancelled):
            frame = utils.get_void_array_1d(self.length)
            for i in range(len(points)):
                if (self.isCancelled):
                    return
                # Clear
                if (not points[i].x in points_contact):
                    frame[points[i].x] = (0, 0, 0, 0)
                # Next move
                velocity = randint(0, 100)
                if (velocity <= turn_chance):
                    points[i].x_v *= -1
                points[i].x += points[i].x_v
                points[i].x %= self.length-1
                if points[i].x in points_location:
                    points_location[points[i].x] += 1
                else:
                    points_location[points[i].x] = 1
                if points[i].x+points[i].x_v in points_location:
                    points_location[points[i].x+points[i].x_v] += 1
                else:
                    points_location[points[i].x+points[i].x_v] = 1
                # Show            
                frame[points[i].x] = (color[0], color[1], color[2], color[3])
            for key, value in points_location.items():
                if (value > 1):
                    points_contact[key] = 1
            for key in list(points_contact.keys()):
                value = points_contact[key]
                frame[key] = (int(contact_color[0]*value), int(contact_color[1]*value), int(contact_color[2]*value), int(contact_color[3]*value))
                points_contact[key] = round(points_contact[key]-0.05, 2)
                if (points_contact[key]  < 0):
                    points_contact.pop(key)

            self._send_frame(frame)
            points_location.clear()
            if (self.isCancelled):
                    return
            time.sleep(wait_ms)
    
    def wheel(self, pos):
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