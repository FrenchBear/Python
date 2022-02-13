# mult_classic_tests.py
# Tests for classic multiplication
#
# 2022-02-13    PV

from mult_classic import mult_classic
import unittest

class TestMultClassic(unittest.TestCase):

    def test_1(self):
        self.assertEqual(mult_classic('8','7'), '56')

    def test_2(self):
        n1 = '12306724243'
        n2 = '4567827480727234'
        res = '56214993194907465938133862'
        self.assertEqual(mult_classic(n1, n2), res)

if __name__ == '__main__':
    unittest.main()
