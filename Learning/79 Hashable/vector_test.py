# testvector.py
# unit tests for vector class

from vector import Vector
import unittest

class TestVectorMethods(unittest.TestCase):

    def test_constructor(self):
        v1 = Vector(0, 1, 2)
        v2 = Vector((0, 1, 2))
        v3 = Vector(range(3))
        self.assertEqual(v1, v2)
        self.assertEqual(v1, v3)

    def test_len(self):
        l1 = len(Vector(1,2,3))
        self.assertEqual(l1, 3)
        self.assertEqual(len(Vector(1)), 1)

    def test_str(self):
        self.assertEqual(str(Vector(3, 4)), '(3.0, 4.0)')      # Vector coord type is float

    def test_repr(self):
        self.assertEqual(repr(Vector(3, 4)), 'Vector([3.0, 4.0])')     # Repr use a list for coords

    def test_iter(self):
        iv = iter(Vector(3,4))
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
        self.assertTrue(v==v1)
        self.assertFalse(v==v2)

    def test_hash(self):
        self.assertEqual(hash(Vector(3, 4)), 7)

if __name__ == '__main__':
    unittest.main()
