import numpy as np
import animations.array_utils as utils

def add_void_layer(arr, init_value=None):
    if type(arr[0]).__name__ != "list":
        arr = [arr]
    new_layer = [init_value] * len(arr[0])    
    arr.insert(0, new_layer)
    return arr

def add_void_layer_2d(arr, init_value=None):
    if type(arr[0][0]).__name__ != "list":
        arr = [arr]
    new_layer = [[init_value] * len(arr[0][0])] * len(arr[0])    
    arr.insert(0, new_layer)
    return arr

init_value = None
x = np.full((3, 5), None)
print(x)
x.fill(init_value)
print(x)

x[0,1] = 2
print(x)
arr = utils.get_colorless_array_2d(3,3)
print(arr)
arr = add_void_layer_2d(arr)
print(arr)

T = [[[None, 1, 1, 1], 
     [1, None, 1, None], 
     [None, 1, None, 1], 
     [1, None, 1, 1]], 
     [[9, None, 9, 9], 
     [9, None, 9, None], 
     [9, 9, 9, 9], 
     [None,9,9,None]],
     [[3, 3, 3, 3], 
     [3, 3, 3, 3], 
     [3, 3, 3, 3], 
     [3,3,3,3]]]

N = [[(1,2,3), 1, 1, 1], 
     [1, None, 1, None], 
     [None, 1, None, 1], 
     [1, None, 1, 1]]

print(type(T).__name__)
print(type(T[0]).__name__)
print(type(T[0][0]).__name__)
print(type(T[0][0][0]).__name__)
print(type(N).__name__)
print(type(N[0]).__name__)
print(type(N[0][0]).__name__)

#array2D = np.array([[31, 12, 43], [21, 9, 16], [0, 9, 0]])
#array2D = np.array(T)
#print("Given array:\n",array2D)
#res = array2D.flatten()
#print("Flattened array:\n ", res)
print(len(T[0]))
print(T[0][0][0])

frame = T[0]
print(frame)

for i, row in enumerate(T[0]):
    for j, column in enumerate(row):
        for k, dim in enumerate(T):
            if T[k][i][j] != None:
                frame[i][j] = T[k][i][j]
                break
print(frame)
F = []
for row in frame:
    F = F + row
print(F)


tup = (10, 10, 10, 10)
tup2 = tuple(10*x for x in tup)

print(tup)
print(tup2)


var = [9,9,9,9,9,9]
print(var)
var = add_void_layer(var,1)
print(var)
var = add_void_layer(var,None)
print(var)

var[0][1] = 7
var[0][3] = 7
var[0][5] = 7
var = add_void_layer(var,None)
var[0][2] = 4


F = [None] * len(var[0])
for i, row in enumerate(zip(*var)):
    for column in row:
        if column != None:
            F[i] = column
            break
        print(column,end = " ")
    print()

print(F)


#for c in array.transpose(1, 0, 2):
#    do_stuff(c)

T = [[-1, -1, -1, 2], [-1, -1, 10, 5], [-1, 1, 12, 5], [12,15,8,6]]
F = [None] * len(T)
for i, row in enumerate(T):
    for column in row:
        if column != -1:
            F[i] = column
            break
        print(column,end = " ")
    print()

print(F)

T = [
        [(None, None, None), (None, None, None), (None, None, None), (2, 2, 2)],
        [(None, None, None), (None, None, None), (10, 10, 10), (5, 5, 5)], 
        [(None, None, None), (1, 1, 1), (12, 12, 12), (5, 5, 5)], 
        [(12, 12, 12), (15, 15, 15), (8, 8, 8), (6, 6, 6)]
    ]

T = [
        [None, None, None, (2, 2, 2)],
        [None, None, (10, 10, 10), (5, 5, 5)], 
        [None, (1, 1, 1), (12, 12, 12), (5, 5, 5)], 
        [(12, 12, 12), (15, 15, 15), (8, 8, 8), (6, 6, 6)]
    ]
F = [None] * len(T)
for i, row in enumerate(T):
    for column in row:
        if column != None:
            F[i] = column
            break
        print(column,end = " ")
    print()

print(F)


N = [(12, 12, 12),(12, 12, 12),(12, 12, 12)]
P = (12, 12, 12)
X = None

print(N)
print(P)
print(X)
print(type(N))
print(type(P))
print(type(X))
print(type(N).__name__)
print(type(P).__name__)
print(type(X).__name__)
print(type(N).__name__ == 'tuple')
print(type(P).__name__ == 'tuple')
print(type(X).__name__ == 'NoneType')

full_frame = [None] * 5 + [(12, 12, 12), (12, 12, 12), (12, 12, 12)] + [None] * 5
print(full_frame)