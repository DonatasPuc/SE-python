import numpy as np

def divide_interval(start, end, parts):
    return np.linspace(start, end, parts+1)

start = -1.3
end = 2.5
parts = 64

intervals = divide_interval(start, end, parts)
print(intervals)