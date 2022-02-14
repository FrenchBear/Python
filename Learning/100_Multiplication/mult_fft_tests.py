# mult_fft_tests.py
# Tests for multiplication using FFT
#
# 2022-02-14    PV

from mult_fft import *
import unittest

class TestMulFFT(unittest.TestCase):

    def test_mult(self):
        n1 = '1234'
        n2 = '5678'
        self.assertEqual(mult_fft(n1, n2), str(int(n1)*int(n2)))
        n1 = '123442'
        n2 = '56788530'
        self.assertEqual(mult_fft(n1, n2), str(int(n1)*int(n2)))
        n1 = '1234423556788530'
        n2 = '5678853012344235'
        self.assertEqual(mult_fft(n1, n2), str(int(n1)*int(n2)))
        n1 = '12344235567885'
        n2 = '5678853012344235'
        self.assertEqual(mult_fft(n1, n2), str(int(n1)*int(n2)))
        n1 = '12344235567885'
        n2 = '567885301234423567567'
        self.assertEqual(mult_fft(n1, n2), str(int(n1)*int(n2)))
if __name__ == '__main__':
    unittest.main()
