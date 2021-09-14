# testvector.py
# unit tests for vector class

from vector import Vector
import unittest
import math


class TestVectorMethods(unittest.TestCase):

    def test_constructor(self):
        v1 = Vector(0, 1, 2)
        v2 = Vector((0, 1, 2))
        v3 = Vector(range(3))
        self.assertEqual(v1, v2)
        self.assertEqual(v1, v3)

    def test_len(self):
        self.assertEqual(len(Vector(1, 2, 3)), 3)
        self.assertEqual(len(Vector([1, 2, 3])), 3)
        self.assertEqual(len(Vector(1)), 1)

    def test_str(self):
        self.assertEqual(str(Vector(3, 4)), '(3.0, 4.0)')      # Vector coord type is float

    def test_repr(self):
        self.assertEqual(repr(Vector(3, 4)), 'Vector([3.0, 4.0])')     # Repr use a list for coords

    def test_iter(self):
        iv = iter(Vector(3, 4))
        self.assertEqual(next(iv), 3)
        self.assertEqual(next(iv), 4)
        with self.assertRaises(StopIteration):
            z = next(iv)

    def test_equals(self):
        v = Vector(3, 4)
        v1 = Vector(3, 4)
        v2 = Vector(3, 4, 5)
        v3 = (3, 4)
        v4 = [3, 4]
        self.assertTrue(v == v1)
        self.assertFalse(v == v2)

    def test_hash(self):
        self.assertEqual(hash(Vector(3, 4)), 7)     # Simple value since hash(3.0) = hash(3)

    def test_bool(self):
        self.assertTrue(bool(Vector(4, 2, -3)))
        self.assertFalse(Vector([0, 0, 0]))

    def test_abs(self):
        self.assertEqual(abs(Vector(-2)), 2)
        self.assertEqual(abs(Vector(3, 4)), 5)
        self.assertAlmostEqual(abs(Vector(1, 2, 3)), math.sqrt(14))

    def test_complex(self):
        self.assertEqual(complex(Vector(3, -2)), 3-2j)
        with self.assertRaises(ValueError):
            c = complex(Vector(1, 2, 3))

    def test_argument(self):
        self.assertAlmostEqual(Vector(3, -2).argument(), -math.atan(2/3))
        with self.assertRaises(ValueError):
            a = Vector(1, 2, 3).argument()

    def test_format(self):
        v = Vector(3,4)
        self.assertEqual(f'{v}', '(3.0, 4.0)')
        self.assertEqual(f'{v:.2r}', '(3.00, 4.00)')
        self.assertEqual(f'{v:.2p}', '(5.00 ∠0.93)')

    def test_shortcuts(self):
        v = Vector(3,4)
        self.assertEqual(v.x, 3)
        self.assertEqual(v.y, 4)
        with self.assertRaises(AttributeError):
            z = v.z

    def test_setattr(self):
        v = Vector(3,4)
        v.Name = 'myVector'
        self.assertEqual(v.Name, 'myVector')
        with self.assertRaises(AttributeError):
            v.z = 2.3

    def test_serialization(self):
        v = Vector(2, 3)
        b = bytes(v)
        v2 = Vector.frombytes(b)
        self.assertEqual(v, v2)

    def test_slices(self):
        v = Vector(range(8))
        self.assertEqual(v[2], 2.0)
        self.assertEqual(v[-1], 7.0)
        self.assertEqual(v[2:7], Vector(2, 3, 4, 5, 6))
        self.assertEqual(v[2:7:2], Vector(2, 4, 6))

if __name__ == '__main__':
    unittest.main()
