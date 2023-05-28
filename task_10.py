import sympy as sp

# Define the symbol and the function
x = sp.Symbol('x')
f = sp.exp(-x)

# Calculate the definite integral
indefinite_integral = sp.integrate(f, x)
definite_integral = sp.integrate(f, (x, 0, 1))

# Print the result
print("Neapibrėžtinis integralas:\n", indefinite_integral)
print("Apibrėžtinis integralas intervale [0,1]:\n", definite_integral)