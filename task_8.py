import numpy as np

matrix = np.array([[1, 2], [3, 4]])
eigenvalues, eigenvectors = np.linalg.eig(matrix)

print("Tikrinės reikšmės:")
print(eigenvalues)

print("\nTikriniai vectoriai:")
print(eigenvectors)