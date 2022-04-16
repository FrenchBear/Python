# c_match_tests.py
# Tests for c_checkargs, verifies Fract constructors using match for type checking
#
# 2022-03-19    PV
# 2022-04-16    PV      Added test cases using math.nan, math.inf and sequences of 2 int

from c_match import *
import unittest
import fractions


class TestOptargs(unittest.TestCase):

    def test_fract(self):
        # Construct from 0, 1 or 2 integers
        self.assertEqual(str(Fract()), '0')
        self.assertEqual(str(Fract(0)), '0')
        self.assertEqual(str(Fract(2)), '2')
        self.assertEqual(str(Fract(-2)), '-2')
        self.assertEqual(str(Fract(2, 3)), '2/3')
        self.assertEqual(str(Fract(-2, 3)), '-2/3')
        self.assertEqual(str(Fract(2, -3)), '-2/3')
        self.assertEqual(str(Fract(-2, -3)), '2/3')
        self.assertEqual(str(Fract(4, 6)), '2/3')
        self.assertEqual(str(Fract(4, 2)), '2')

        # Construct from a fractions.Fraction (Python library)
        self.assertEqual(str(Fract(fractions.Fraction(2, 3))), '2/3')

        # Construct from a Fract
        self.assertEqual(str(Fract(Fract(2, 3))), '2/3')

        # Convert from double
        self.assertEqual(str(Fract(0.25)), '1/4')
        self.assertEqual(str(Fract(0.3333333)), '1/3')
        self.assertEqual(str(Fract(3.1415926535)), '355/113')
        self.assertEqual(str(Fract(-0.0)), '0')

        # Convert from sequence of 2 integers
        self.assertEqual(str(Fract([2, 8])), '1/4')
        self.assertEqual(str(Fract((3, 6))), '1/2')
        self.assertEqual(str(Fract(range(4,6))), '4/5')

        # Check invalid cases
        with self.assertRaises(TypeError):
            f = Fract(1, 2, 3)
        with self.assertRaises(ZeroDivisionError):
            f = Fract(1, 0)
        with self.assertRaises(ValueError):
            f = Fract(0.5, 2)
        with self.assertRaises(TypeError):
            f = Fract('hello')
        with self.assertRaises(ValueError):
            f = Fract(math.nan)
        with self.assertRaises(OverflowError):
            f = Fract(math.inf)

if __name__ == '__main__':
    unittest.main()
