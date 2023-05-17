import numpy as np

array = np.random.rand(5, 5)
sorted_array = array[array[:, 1].argsort()]
print(sorted_array)