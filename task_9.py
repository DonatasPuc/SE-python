import numpy as np
import sympy as sp


poly_func = np.poly1d([0.5, 5, 4])
derivative = np.poly1d(poly_func).deriv()
print("Derivative using numpy:", derivative)


x = sp.symbols('x')
f = 0.5 * x**2 + 5 * x + 4
derivative = sp.diff(f, x)
print("Derivative using sympy:\n", derivative)