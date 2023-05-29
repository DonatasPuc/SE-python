import numpy as np

def main():
    N = int(input('Input N x N array dimention N: '))
    array = np.fromfunction(lambda i, j: i + j, (N, N), dtype=int)
    print(array)

if __name__ == '__main__':
    main()