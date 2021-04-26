# f1_test.py
# unit tests for f1.py

from f1 import cube
import unittest


class TestNumericalMethods(unittest.TestCase):

    def test_cube(self):
        c1 = cube(3)
        self.assertEqual(c1, 27)
