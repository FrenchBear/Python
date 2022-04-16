# b_checkargs_tests.py
# Tests for b_checkargs, verifies Fract constructors
#
# 2022-03-19    PV

from b_checkargs import *
import unittest
import fractions

class TestOptargs(unittest.TestCase):

    def test_fract(self):
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

        self.assertEqual(str(Fract(fractions.Fraction(2,3))), '2/3')

        self.assertEqual(str(Fract(Fract(2,3))), '2/3')

        self.assertEqual(str(Fract(0.25)), '1/4')
        self.assertEqual(str(Fract(0.3333333)), '1/3')
        self.assertEqual(str(Fract(3.1415926535)), '355/113')

        with self.assertRaises(TypeError):
            f = Fract(1, 2, 3)
        with self.assertRaises(ZeroDivisionError):
            f = Fract(1, 0)
        with self.assertRaises(ValueError):
            f = Fract(0.5, 2)

        with self.assertRaises(TypeError):
            f = Fract('hello')


if __name__ == '__main__':
    unittest.main()
