import numpy as np
import matplotlib.pyplot as plt

# Prompt the user to input D
D = float(input("Įveskite dispersiją (D): "))
# Prompt the user to input V
V = float(input("Įveskite vidurkį (V): "))

random_numbers = np.random.normal(V, D, 1000)

# Create a histogram
plt.hist(random_numbers, bins=30, density=True)
plt.title('Random Numbers (Normal Distribution)')
plt.xlabel('Value')
plt.ylabel('Frequency')

plt.show()
