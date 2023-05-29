# Lab4 consists of 3 parts
## 1. Extending Python with C
A GCD function is implemented with error handling in C and latter used in python gcd.py script.

To build gcd_module in order to latter use it in gcd.py do these steps:
```
python3 setup.py build
mv build/lib*/*.so .
```

## 2. Implemented new RationalNumber data type in Python
Example usage:
```python
>>> from rational_number import RationalNumber
>>> r1=RationalNumber(1,2)
>>> r2=RationalNumber(8,9)
>>> print(r1 * r2)
4/9
>>> print(r1 * r2 * 8)
32/9
```
Note: RationalNumber is using using gcd module implemented in part 1. So building it is required for RationalNumber to work. Alternatively use math.gcd().

## 3. Embedding Python in C
An example how to use the RationalNumber data type (implemented in part 2) in C code.

Execution steps. In command line run:
```
make rational
make run
make clean
```