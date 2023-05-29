import numpy as np

def generate_random_array(size, min_val, max_val):
    return np.random.randint(min_val, max_val+1, size=size)

def construct_repeating_array(arr, N):
    arr = np.array(arr)
    return np.tile(arr, N)

def main():
    N = 5
    array_size = 10

    array = generate_random_array(array_size, 0, array_size)
    repeated_array = construct_repeating_array(array, N)
    print(repeated_array)

if __name__ == '__main__':
    main()