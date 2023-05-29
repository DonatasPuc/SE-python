# Lab4 consists of 3 parts
## 1. Extending Python with C
A GCD function is implemented with error handling in C and latter used in python gcd.py script.

To build gcd_module in order to latter use it in gcd.py do these steps:
```
python3 setup.py build
mv build/lib*/*.so .
```

## 2. Implemented new rational_number data type in Python

## 3. Embedding Python in C