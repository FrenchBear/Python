# mult_karatsuba_tests.py
# Tests for multiplication using Karatsuba algorithm
#
# 2022-02-13    PV

from mult_karatsuba import *
import unittest

class TestMultKaratsuba(unittest.TestCase):

    def test_compare(self):
        self.assertEqual(ns_compare('12','345'), -1)
        self.assertEqual(ns_compare('123','34'), 1)
        self.assertEqual(ns_compare('123','123'), 0)
        self.assertEqual(ns_compare('123','321'), -1)
        self.assertEqual(ns_compare('321','123'), 1)
        self.assertEqual(ns_compare('1','0'), 1)

        self.assertEqual(ns_compare('-12','-345'), 1)
        self.assertEqual(ns_compare('-123','-34'), -1)
        self.assertEqual(ns_compare('-123','-123'), 0)
        self.assertEqual(ns_compare('-123','-321'), 1)
        self.assertEqual(ns_compare('-321','-123'), -1)
        self.assertEqual(ns_compare('-1','0'), -1)

        self.assertEqual(ns_compare('-12','345'), -1)
        self.assertEqual(ns_compare('-123','34'), -1)
        self.assertEqual(ns_compare('-123','123'), -1)
        self.assertEqual(ns_compare('-123','321'), -1)
        self.assertEqual(ns_compare('-321','123'), -1)
        self.assertEqual(ns_compare('-1','0'), -1)

        self.assertEqual(ns_compare('12','-345'), 1)
        self.assertEqual(ns_compare('123','-34'), 1)
        self.assertEqual(ns_compare('123','-123'), 1)
        self.assertEqual(ns_compare('123','-321'), 1)
        self.assertEqual(ns_compare('321','-123'), 1)
        self.assertEqual(ns_compare('1','0'), 1)

        self.assertEqual(ns_compare('0','0'), 0)
        self.assertEqual(ns_compare('0','-0'), 0)
        self.assertEqual(ns_compare('-0','0'), 0)
        self.assertEqual(ns_compare('-0','-0'), 0)

    def test_add(self):
        self.assertEqual(ns_add('12','345'), '357')
        self.assertEqual(ns_add('345','12'), '357')
        self.assertEqual(ns_add('12','-345'), '-333')
        self.assertEqual(ns_add('345','-12'), '333')
        self.assertEqual(ns_add('-12','345'), '333')
        self.assertEqual(ns_add('-345','12'), '-333')
        self.assertEqual(ns_add('-12','-345'), '-357')
        self.assertEqual(ns_add('-345','-12'), '-357')

    def test_mult(self):
        n1 = '1234'
        n2 = '5678'
        self.assertEqual(mult_karatsuba(n1, n2), str(int(n1)*int(n2)))
        n1 = '123442'
        n2 = '56788530'
        self.assertEqual(mult_karatsuba(n1, n2), str(int(n1)*int(n2)))
        n1 = '1234423556788530'
        n2 = '5678853012344235'
        self.assertEqual(mult_karatsuba(n1, n2), str(int(n1)*int(n2)))
        n1 = '12344235567885'
        n2 = '5678853012344235'
        self.assertEqual(mult_karatsuba(n1, n2), str(int(n1)*int(n2)))
        n1 = '12344235567885'
        n2 = '567885301234423567567'
        self.assertEqual(mult_karatsuba(n1, n2), str(int(n1)*int(n2)))

if __name__ == '__main__':
    unittest.main()
