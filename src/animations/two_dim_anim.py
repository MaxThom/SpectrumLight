import time
import math
import animations.array_utils as utils
import animations.img_utils as img_utils
from animations.anim import __Anim
from random import *
from skimage import io, transform
import numpy as np
import os
from PIL import Image

class TwoDimAnim(__Anim):
    def __init__(self, p_display, p_segment, p_mutex):
        super().__init__(p_display, p_segment, p_mutex)
        self.start_index = (p_segment[0], p_segment[1])
        self.end_index = (p_segment[2], p_segment[3])
        self.width = self.end_index[0] - self.start_index[0] + 1
        self.height = self.end_index[1] - self.start_index[1] + 1
        print(self.start_index, self.end_index)
        print(self.width, self.height)

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

        # Add sub
        full_frame = utils.get_void_array_2d(self.display.get_num_pixels_2d()[0], self.display.get_num_pixels_2d()[1])
        full_frame[self.start_index[1]:self.end_index[1]+1, self.start_index[0]:self.end_index[0]+1] = flatten_frame

        frame = full_frame.flatten()
        #print("locked")
        if self.mutex.acquire():
        #print("unlocked")
            self.display.send_frame(frame)

    def __clear(self):
        self.__send_frame(utils.get_colorless_array_2d(self.width, self.height))

    def off(self, args):
        self.__clear()

    #
    # Args: image_name, image_ratio, frame_time_sec
    #
    def image_display(self, args):
        image_name = args["image_name"] if "image_name" in args else "Ninject.png"
        image_ratio = args["image_ratio"] if "image_ratio" in args else "fit" # or fill
        if image_name.endswith(".gif"):
            self.gif_display(args)
            return

        img_frame = None
        processed_image_name = f"{image_name}_{image_ratio}_{self.width}_{self.height}"
        if os.path.isfile(f'../anim_frames_processed/{processed_image_name}'):
            with open(f'../anim_frames_processed/{processed_image_name}', 'rb') as f:
                img_frame = np.load(f, allow_pickle=True)
        else:
            # Read and resize image
            img = io.imread(f'../anim_frames/{image_name}')
            img_width, img_height = (None, None)
            if image_ratio == "fit":
                img_width, img_height = img_utils.adjust_image_to_size(img.shape[1], img.shape[0], self.width, self.height)
            elif image_ratio == "fill":
                img_width, img_height = (self.width, self.height)
            img_resized = img_utils.resize_image(img, img_width, img_height)
            
            # Transform array to tuple
            img_frame = img_utils.transform_image_color_to_tuple(img_height, img_width, img_resized)

            # Save processed image
            with open(f'../anim_frames_processed/{processed_image_name}', 'wb') as f:
                np.save(f, img_frame)

        # Center image
        frame = img_utils.center_image_frame(self.width, self.height, img_frame)
        
        #print(frame)
        self.__send_frame(frame)

        # Todo
        # 1. [x] - Make it work for under 48 pixels
        # 2. [x] - Use better library for loading speed and resize (only if bigger than 48)
        # 3. [x] - Center image in frame
        # 4. [x] - Save image
        # 5. [x] - Load image
        # 6. [x] - Settings frame [image_path, ratio]
        # 7. [] - Make it work for gifs

    #
    # Args: image_name, image_ratio, frame_time_sec
    #
    def image_display2(self, args):
        image_name = args["image_name"] if "image_name" in args else "Ninject.png"
        image_ratio = args["image_ratio"] if "image_ratio" in args else "fit" # or fill
        if image_name.endswith(".gif"):
            self.gif_display(args)
            return

        img_frame = None
        processed_image_name = f"{image_name}_{image_ratio}_{self.width}_{self.height}"
        if os.path.isfile(f'../anim_frames_processed/{processed_image_name}'):
            with open(f'../anim_frames_processed/{processed_image_name}', 'rb') as f:
                img_frame = np.load(f, allow_pickle=True)
        else:
            # Read and resize image
            im = Image.open(f'../anim_frames/{image_name}')
            img = np.asarray(im)
            img_width, img_height = (None, None)
            if image_ratio == "fit":
                img_width, img_height = img_utils.adjust_image_to_size(img.shape[1], img.shape[0], self.width, self.height)
            elif image_ratio == "fill":
                img_width, img_height = (self.width, self.height)
            img_resized = img_utils.resize_image(im, img_width, img_height)
            
            # Transform array to tuple
            img_frame = img_utils.transform_image_color_to_tuple(img_height, img_width, img_resized)

            # Save processed image
            with open(f'../anim_frames_processed/{processed_image_name}', 'wb') as f:
                np.save(f, img_frame)

        # Center image
        frame = img_utils.center_image_frame(self.width, self.height, img_frame)
        
        #print(frame)
        self.__send_frame(frame)

    #
    # Args: image_name, image_ratio, frame_time_sec
    #
    def gif_display(self, args):
        image_name = args["image_name"] if "image_name" in args else "Ninject.png"
        image_ratio = args["image_ratio"] if "image_ratio" in args else "fit" # or fill
        frame_time_sec = args["frame_time_sec"] if "frame_time_sec" in args else 0.2
        gif_frames = []
        processed_image_name = f"{image_name}_{image_ratio}_{self.width}_{self.height}"
        if os.path.isfile(f'../anim_frames_processed/{processed_image_name}'):
            try:
                with open(f'../anim_frames_processed/{processed_image_name}', 'rb') as f:
                    while True:
                        gif_frames.append(np.load(f, allow_pickle=True))
            except OSError:
                pass # end of sequence
        else:
            # Read and resize image
            gif = Image.open(f'../anim_frames/{image_name}')
            try:
                gif_frames.append(self.__gif_transform(gif, image_ratio))
                print(gif)
                while 1:
                    gif.seek(gif.tell()+1)
                    gif_frames.append(self.__gif_transform(gif, image_ratio))
                    print(gif)
            except EOFError:
                pass # end of sequence
            with open(f'../anim_frames_processed/{processed_image_name}', 'wb') as f:
                for frame in gif_frames:
                    np.save(f, frame)

        while True:
            if (self.isCancelled):
                return
            for img_frame in gif_frames:
                # Center image
                frame = img_utils.center_image_frame(self.width, self.height, img_frame)
                time.sleep(frame_time_sec)
                if (self.isCancelled):
                    return                
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
        #start = 0 if not reverse else self.length-1
        #end = -1 if reverse else self.length
        #step = 1 if not reverse else -1
        
        """Wipe color across display a pixel at a time."""
        while True:
            self.__clear()
            frame = utils.get_colorless_array_2d(self.width, self.height)
            for i in range(len(frame)):

                for j in range(len(frame[i])):
                    frame[i][j] = color
                    self.__send_frame(frame)
                    if (self.isCancelled):
                        return
                    time.sleep(wait_ms)

    def __gif_transform(self, gif_frame, image_ratio):
        im = gif_frame.convert('RGBA')                    
        im_array = np.asarray(im)

        img_width, img_height = (None, None)
        if image_ratio == "fit":
            img_width, img_height = img_utils.adjust_image_to_size(im_array.shape[1], im_array.shape[0], self.width, self.height)
        elif image_ratio == "fill":
            img_width, img_height = (self.width, self.height)

        img_resized = img_utils.resize_image(im, img_width, img_height)
        img_frame = img_utils.transform_image_color_to_tuple(img_height, img_width, img_resized)

        return img_frame
    
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