import numpy as np

def main():
    matrix = np.array([[1, 2], [3, 4]])
    eigenvalues, eigenvectors = np.linalg.eig(matrix)

    print("Tikrinės reikšmės:")
    print(eigenvalues)

    print("\nTikriniai vectoriai:")
    print(eigenvectors)

if __name__ == '__main__':
    main()