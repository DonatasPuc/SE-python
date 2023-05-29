# Autorius: Donatas Pučinskas, 3 kursas, 4 grupė
import doctest
import unittest
import main.gcd

from main.gcd import find_gcd

class TestFindGcd(unittest.TestCase):
    def test_gcd_with_prime_numbers(self):
        self.assertEqual(find_gcd(13, 17), 1)

    def test_gcd_with_one(self):
        self.assertEqual(find_gcd(1, 20), 1)
        self.assertEqual(find_gcd(20, 1), 1)

    def test_gcd_with_same_numbers(self):
        self.assertEqual(find_gcd(20, 20), 20)

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(main.gcd))
    return tests