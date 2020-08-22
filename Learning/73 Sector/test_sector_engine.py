# test_sector_engine.py
# Units tests for Sector engine
# 2020-08-21    PV

import sector_engine
import unittest


class TestSectorEngine(unittest.TestCase):

    def test_XY1(self):
        se = sector_engine.sector_engine()
        self.assertEqual(se.NE_dir(-1, -1), 5)
        self.assertEqual(se.NE_dir(-1, 0), 6)
        self.assertEqual(se.NE_dir(-1, 1), 7)
        self.assertEqual(se.NE_dir(0, -1), 4)
        self.assertEqual(se.NE_dir(0, 1), 0)
        self.assertEqual(se.NE_dir(1, -1), 3)
        self.assertEqual(se.NE_dir(1, 0), 2)
        self.assertEqual(se.NE_dir(1, 1), 1)

    def test_XY2(self):
        se = sector_engine.sector_engine()
        self.assertEqual(se.dir_NE(0), (0, 1))
        self.assertEqual(se.dir_NE(1), (1, 1))
        self.assertEqual(se.dir_NE(2), (1, 0))
        self.assertEqual(se.dir_NE(3), (1, -1))
        self.assertEqual(se.dir_NE(4), (0, -1))
        self.assertEqual(se.dir_NE(5), (-1, -1))
        self.assertEqual(se.dir_NE(6), (-1, 0))
        self.assertEqual(se.dir_NE(7), (-1, 1))

    def test_XY3(self):
        se = sector_engine.sector_engine()
        for dir_N in range(-1, 2):
            for dir_E in range(-1, 2):
                if dir_N != 0 or dir_E != 0:
                    dir = se.NE_dir(dir_N, dir_E)
                    (N,E) = se.dir_NE(dir)
                    self.assertEqual(dir_N, N)
                    self.assertEqual(dir_E, E)


if __name__ == '__main__':
    unittest.main()
