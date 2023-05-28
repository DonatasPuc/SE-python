import numpy as np

arr = np.zeros((10,10), dtype=int)
arr = np.pad(arr, ((1,),(1,)), constant_values=(1))
print(arr)