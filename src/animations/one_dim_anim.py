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

    # Flatten and send frame
    def __send_frame(self, next_frame):
        frame = None
        if type(next_frame[0]).__name__ == "list":
            frame = [None] * len(next_frame[0])
            for i, row in enumerate(zip(*next_frame)):
                for column in row:
                    if column != None:
                        frame[i] = column
                        break
        else:
            frame = next_frame
        self.display.send_frame(self.start_index, frame)

    def __clear(self):
        self.__send_frame(utils.get_colorless_array_1d(self.length))

    def off(self, args):
        self.__clear()

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
                time.sleep(wait_ms / 1000.0)

    #
    # Args: color, wait_ms, reverse, fade_step
    #
    def color_wipe_fade(self, args):
        color = utils.array_to_tuple(args["color"]) if "color" in args else (0,0,255)
        if len(color) == 3:
            color = (color[0], color[1], color[2], 0)
        wait_ms = args["wait_ms"] if "wait_ms" in args else 0.05
        reverse = args["reverse"] if "reverse" in args else False
        fade_step = args["fade_step"] if "fade_step" in args else 50
        start = 0 if not reverse else self.length-1
        end = -1 if reverse else self.length
        step = 1 if not reverse else -1

        step_c = self.length * max(abs(100 - fade_step), 1) / 50
        step_r = color[0] / step_c
        step_g = color[1] / step_c
        step_b = color[2] / step_c
        step_w = color[3] / step_c
        while (True):
            for i in range(start, end, step):
                frame = utils.get_void_array_1d(self.length)
                if not reverse:
                    for j in range(i+1):
                        if (j < i-1): 
                            r = int(max(0, color[0] - (i-j) * step_r))
                            g = int(max(0, color[1] - (i-j) * step_g))
                            b = int(max(0, color[2] - (i-j) * step_b))
                            w = int(max(0, color[3] - (i-j) * step_w))                        
                            frame[j] = (r, g, b, w)
                        else:
                            frame[j] = color                        
                else:
                    for j in range(start, i+1, step):
                        if j > i+1: 
                            r = int(max(0, color[0] - (i-j) * step_r))
                            g = int(max(0, color[1] - (i-j) * step_g))
                            b = int(max(0, color[2] - (i-j) * step_b))
                            w = int(max(0, color[3] - (i-j) * step_w))                        
                            frame[j] = (r, g, b, w)
                        else:
                            frame[j] = color
                self.__send_frame(frame)
                if (self.isCancelled):
                    return
                time.sleep(wait_ms/1000)
                if (self.isCancelled):
                    return
    
    #
    # Args: wait_ms, color_step, fade_step
    #
    def color_wipe_rainbow(self, args):
        color_step = args["color_step"] if "color_step" in args else 30
        wait_ms = args["wait_ms"] if "wait_ms" in args else 0.05
        fade_step = args["fade_step"] if "fade_step" in args else 50

        step = self.length * max(abs(100 - fade_step), 1) / 50
        while (True):
            for k in range(256):
                cycle_color = self.__wheel(((256 // self.length + k*color_step)) % 256) 
                step_r = cycle_color[0] / step
                step_g = cycle_color[1] / step
                step_b = cycle_color[2] / step
                for i in range(self.length):
                    frame = utils.get_void_array_1d(self.length)
                    for j in range(i+1):
                        if (j < i-1):
                            r = int(max(0, cycle_color[0] - (i-j) * step_r))
                            g = int(max(0, cycle_color[1] - (i-j) * step_g))
                            b = int(max(0, cycle_color[2] - (i-j) * step_b))
                            frame[j] = (r, g, b)
                        else:
                            frame[j] = (cycle_color[0], cycle_color[1], cycle_color[2])
                    self.__send_frame(frame)
                    if (self.isCancelled):
                        return
                    time.sleep(wait_ms)
                    if (self.isCancelled):
                        return

    #
    # Args: wait_ms, color1, color2, size1, size2, with_animation, fade_step
    #
    def color_pair(self, args):
        color1 = utils.array_to_tuple(args["color1"]) if "color1" in args else (255,0,0,0)
        color2 = utils.array_to_tuple(args["color2"]) if "color2" in args else (0,0,255,0)
        wait_ms = args["wait_ms"] if "wait_ms" in args else 0.05
        size1 = args["size1"] if "size1" in args else 3
        size2 = args["size2"] if "size2" in args else 3
        with_animation = args["with_animation"] if "with_animation" in args else False
        fade_step = args["fade_step"] if "fade_step" in args else 50

        self.__clear()
            
        i = 0
        frame = utils.get_void_array_1d(self.length)
        while i < self.length:            
            for j in range(i, i+size1):
                if j >= self.length:
                    break
                frame[j] = (color1[0], color1[1], color1[2],  color1[3])
            i += size1

            for j in range(i, i+size2):
                if j >= self.length:
                    break
                frame[j] = (color2[0], color2[1], color2[2],  color2[3])
            i += size2

            if (self.isCancelled):
                return        
        self.__send_frame(frame)

        if (with_animation):
            #frame = utils.add_void_layer_1d(frame)
            step_tuple = (fade_step, fade_step, fade_step, fade_step)
            color1 = tuple(map(lambda i, j: i-j if i - j > 0 else 0, color1, step_tuple)) 
            color2 = tuple(map(lambda i, j: i-j if i - j > 0 else 0, color2, step_tuple))

            while (True):            
                for l in range(self.length):
                    i = 0
                    while i < self.length:
                        for j in range(i, i+size1):
                            if j >= self.length:
                                break
                            frame[j] = (color1[0], color1[1], color1[2])
                        i += size1

                        for j in range(i, i+size2):
                            if j >= self.length:
                                break
                            frame[j] = (color2[0], color2[1], color2[2])
                        i += size2

                        if (self.isCancelled):
                            return        
                    
                    c = self.display.get_pixels_color_rgbw(l)
                    r = c.r
                    if (r > 0): r = int(max(0, c.r + fade_step))
                    g = c.g
                    if (g > 0): g = int(max(0, c.g + fade_step))
                    b = c.b
                    if (b > 0): b = int(max(0, c.b + fade_step))                
                    
                    frame[l] = (r, g, b)
                    k = 5
                    for j in range(l+1, l+5):
                        if (j < self.length):
                            c = self.display.get_pixels_color_rgbw(j)
                            r = c.r
                            if (r > 0): r = int(max(0, c.r + (fade_step/5 * k)))
                            g = c.g
                            if (g > 0): r = int(max(0, c.g + (fade_step/5 * k)))
                            b = c.b
                            if (b > 0): r = int(max(0, c.b + (fade_step/5 * k)))
                            frame[j] = (r, g, b)
                        k -= 1
                    k = 1
                    for j in range(l-5, l-1):
                        if (j >= 0):
                            c = self.display.get_pixels_color_rgbw(j)
                            r = c.r
                            if (r > 0): r = int(max(0, c.r + (fade_step/5 * k)))
                            g = c.g
                            if (g > 0): r = int(max(0, c.g + (fade_step/5 * k)))
                            b = c.b
                            if (b > 0): r = int(max(0, c.b + (fade_step/5 * k)))
                            frame[j] = (r, g, b)
                        k += 1

                    self.__send_frame(frame)
                    if (self.isCancelled):
                        return
                    time.sleep(wait_ms)
                    if (self.isCancelled):
                        return

    #
    # Args: wait_ms
    #
    def rainbow_cycle(self, args):
        wait_ms = args["wait_ms"] if "wait_ms" in args else 0.05
        self.__clear()
        while True:
            for j in range(256): # one cycle of all 256 colors in the wheel
                frame = utils.get_void_array_1d(self.length)
                for i in range(self.length):
                    frame[i] = self.__wheel(((i * 256 // self.length) + j) % 256)
                if (self.isCancelled):
                    return
                self.__send_frame(frame)
                if wait_ms > 0:
                    time.sleep(wait_ms)
                if (self.isCancelled):
                    return

    #
    # Args: wait_ms, count, turn_chance, color, contact_color
    #
    def labyrinth(self, args):
        # Init arguments
        wait_ms = args["wait_ms"] if "wait_ms" in args else 0.05
        count = args["count"] if "count" in args else 10
        turn_chance = args["turn_chance"] if "turn_chance" in args else 2
        color = utils.array_to_tuple(args["color"]) if "color" in args else (0,0,255,0)
        contact_color = utils.array_to_tuple(args["contact_color"]) if "contact_color" in args else (127, 127, 127, 0)

        self.__clear()
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

            self.__send_frame(frame)
            points_location.clear()
            if (self.isCancelled):
                    return
            time.sleep(wait_ms)
    
    #
    # Args: wait_ms, blink_time, color
    #
    def blink_color(self, args):
        wait_ms = args["wait_ms"] if "wait_ms" in args else 1
        blink_time = args["blink_time"] if "blink_time" in args else 3
        color = utils.array_to_tuple(args["color"]) if "color" in args else (0,0,255,0)

        self.__clear()
        while True:
            self.__clear()
            for j in range(blink_time):
                frame = utils.get_void_array_1d(self.length)
                for k in range(self.length):
                   frame[k] =(color[0], color[1], color[2],  color[3])
                if self.isCancelled:
                    return
                self.__send_frame(frame)
                time.sleep(0.08)
                self.__clear()
                if self.isCancelled:
                    return
                time.sleep(0.08)
                if self.isCancelled:
                    return
            time.sleep(wait_ms)
            if self.isCancelled:
                return

    #
    # Args: wait_ms,  color, size
    #
    def appear_from_back(self, args):
        wait_ms = args["wait_ms"] if "wait_ms" in args else 0.02
        size = args["size"] if "size" in args else 3
        color = utils.array_to_tuple(args["color"]) if "color" in args else (0,0,255,0)

        self.__clear()
        while not self.isCancelled:
            for i in range(int(self.length/size)):
                for j in reversed(range(i*size, self.length-size)):
                    frame = utils.get_colorless_array_1d(self.length)
                    if self.isCancelled:
                        return
                    # first set all pixels at the begin
                    for k in range(i*size):
                        frame[k] = (color[0], color[1], color[2],  color[3])
                    # set then the pixel at position j
                    for l in range(size):
                        frame[j+l] = (color[0], color[1], color[2],  color[3])
                    if self.isCancelled:
                        return
                    self.__send_frame(frame)
                    time.sleep(wait_ms)
                    if self.isCancelled:
                        return

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