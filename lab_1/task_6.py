import numpy as np

N = int(input('Input N x N array dimention N: '))
array = np.fromfunction(lambda i, j: i + j, (N, N), dtype=int)
print(array)