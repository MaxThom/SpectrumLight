


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