# Autorius: Donatas Pučinskas, 3 kursas, 4 grupė

def find_gcd(a: int, b: int) -> int:
    """
    Compute the greatest common divisor of a and b.

    >>> find_gcd(20, 15)
    5
    >>> find_gcd(20, 0)
    20
    >>> find_gcd(-20, -15)
    5
    """
    while b:
        a, b = b, a % b
    return abs(a)