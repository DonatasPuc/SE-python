import numpy as np

def main():
    array = np.random.rand(5, 5)
    sorted_array = array[array[:, 1].argsort()]
    print(sorted_array)

if __name__ == '__main__':
    main()