from dataclasses import dataclass
import numpy as np

def get_void_array_1d(length, init_value=None):
    return [init_value] * length

def get_colorless_array_1d(length):
    return [(0, 0, 0)] * length

def get_void_array_2d(height, width, init_value=None):
    x = None
    if type(init_value).__name__ == 'tuple':
        x = np.empty((height, width), dtype=tuple)
        x.fill(init_value)
    else:
        x = np.full((height, width), init_value)    
    return x

def get_colorless_array_2d(height, width):
    return get_void_array_2d(height, width, (0,0,0))

def array_to_tuple(array):
    return tuple(array)

def add_void_layer_1d(array, init_value=None):
    if type(array[0]).__name__ != "list":
        array = [array]
    new_layer = [init_value] * len(array[0])    
    array.insert(0, new_layer)
    return array

def add_void_layer_2d(arr, init_value=None):
    if type(arr[0][0]).__name__ != "list":
        arr = [arr]
    new_layer = [[init_value] * len(arr[0][0])] * len(arr[0])    
    arr.insert(0, new_layer)
    return arr

def multiply_tuple_by_scalar(tup, scalar):
    return tuple(scalar * x for x in tup)

def floor_tuple(tup):
    return tuple(int(x) for x in tup)

def divide_tuple_by_scalar(tup, scalar):
    return tuple(scalar // x for x in tup)

@dataclass
class Point:
    x: int
    x_v: int
    y: int = 0    
    y_v: int = 0