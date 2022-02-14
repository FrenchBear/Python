# mult_classic.py
# Classic implementation of multiplication algorithm
#
# 2022-02-11    PV

import math

SLICE_LEN = 2
SLICE_VAL = 10**SLICE_LEN


def mult_classic(n1: str, n2: str) -> str:
    len1 = math.ceil(len(n1)/SLICE_LEN)
    len2 = math.ceil(len(n2)/SLICE_LEN)
    n1 = '0'*(SLICE_LEN*len1-len(n1))+n1
    n2 = '0'*(SLICE_LEN*len2-len(n2))+n2
    t1 = [int(n1[i:i+SLICE_LEN]) for i in range(len(n1)-SLICE_LEN, -1, -SLICE_LEN)]
    t2 = [int(n2[i:i+SLICE_LEN]) for i in range(len(n2)-SLICE_LEN, -1, -SLICE_LEN)]

    tr = [0] * (len1+len2)
    for i in range(len1):
        if t1[i] != 0:
            for j in range(len2):
                c = t1[i]*t2[j]
                tr[i+j] += c
                if tr[i+j] >= SLICE_VAL:
                    tr[i+j+1] += tr[i+j]//SLICE_VAL
                    tr[i+j] %= SLICE_VAL

    # Eliminate non-significant 0 ahead result if present
    return ''.join(str(c).zfill(SLICE_LEN) for c in tr[::-1]).lstrip('0')


if __name__ == '__main__':
    n1 = '12306724243'
    n2 = '4567827480727234'

    #n1 = '999999999999999999999999999'
    #n2 = '9999999999999999999999999999'

    print(mult_classic(n1, n2))
    print(int(n1)*int(n2))
