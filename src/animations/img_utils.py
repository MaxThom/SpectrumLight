from skimage import io, transform
import numpy as np
import os
import animations.array_utils as utils

def adjust_image_to_size(original_width, original_height, MAX_WIDTH, MAX_HEIGHT):    
    if original_width > original_height:        
        width = int(MAX_WIDTH)
        height = int(original_height / (original_width / MAX_WIDTH))
        if height > MAX_HEIGHT:            
            width = int(width / (height / MAX_HEIGHT))
            height = int(MAX_HEIGHT)
    else:
        height = int(MAX_HEIGHT)
        width = int(original_width / (original_height / MAX_HEIGHT))
        if width > MAX_WIDTH:            
            height = int(height / (width / MAX_WIDTH))
            width = int(MAX_WIDTH)
            
    return width, height

def resize_image(img, img_width, img_height):
    img_resized = transform.resize(img, (img_width, img_height), anti_aliasing=True)
    img_resized = 255 * img_resized
    img_resized = img_resized.astype(np.uint8)
    return img_resized

def transform_image_color_to_tuple(img_height, img_width, img):
    img_frame = utils.get_colorless_array_2d(img_height, img_width)
    for ix,iy,iz in np.ndindex(img.shape):
        img_frame[ix,iy] = utils.array_to_int_tuple(img[ix,iy])
    return img_frame

def center_image_frame(width, height, img):
    frame = utils.get_colorless_array_2d(height, width)
    start_y = int((frame.shape[0] - img.shape[0]) / 2)
    start_x = int((frame.shape[1] - img.shape[1]) / 2)
    frame[start_y:start_y+img.shape[0], start_x:start_x+img.shape[1]] = img
    return frame
