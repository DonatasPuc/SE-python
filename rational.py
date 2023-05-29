from gcd import find_gcd

class RationalNumber:
    """A data type representing a rational number."""

    def __init__(self, numerator: int, denominator: int):
        """
        Initialize a new RationalNumber.

        Args:
            numerator (int): The numerator of the rational number.
            denominator (int): The denominator of the rational number. Must not be zero.

        Raises:
            ValueError: If denominator is zero.
        """
        if denominator == 0:
            raise ValueError("Denominator cannot be zero.")
        
        self.numerator = numerator
        self.denominator = denominator

        # Simplify the fraction
        self.simplify()

    def simplify(self):
        """
        Simplify the RationalNumber to its simplest form.

        Returns:
            None
        """
        gcd = find_gcd(self.numerator, self.denominator)
        self.numerator = self.numerator // gcd
        self.denominator = self.denominator // gcd

    def __mul__(self, other):
        """
        Multiply this RationalNumber by another RationalNumber or an Integer.

        Args:
            other (RationalNumber, int): The RationalNumber or Integer to multiply by.

        Returns:
            RationalNumber: The product of the multiplication.
        """
        if isinstance(other, RationalNumber):
            result = RationalNumber(self.numerator * other.numerator, self.denominator * other.denominator)
        elif isinstance(other, int):
            result = RationalNumber(self.numerator * other, self.denominator)
        else:
            raise ValueError("Can only multiply by another RationalNumber or an integer.")
        
        result.simplify()
        return result

    def __repr__(self):
        """
        Return a string representation of the RationalNumber.

        Returns:
            str: A string representation of the RationalNumber.
        """
        return f"{self.numerator}/{self.denominator}"
