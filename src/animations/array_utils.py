from dataclasses import dataclass

def get_void_array_1d(length, init_value=None):
    return [init_value] * length

def get_colorless_array_1d(length):
    return [(0, 0, 0)] * length

def array_to_tuple(array):
    return tuple(array)

def add_void_layer_1d(array, init_value=None):
    if type(array[0]).__name__ != "list":
        array = [array]
    new_layer = [init_value] * len(array[0])    
    array.insert(0, new_layer)
    return array

@dataclass
class Point:
    x: int
    x_v: int
    y: int = 0    
    y_v: int = 0