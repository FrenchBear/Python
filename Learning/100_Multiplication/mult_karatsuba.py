# mult_karatsuba.py
# Multiplication using Karatsuba algorithm
# n1 = a+b.10^k
# n2 = c+d.10^k
# n1.n2 = ac - ((a-b)(c-d)-ac-bd).10^k + bd.10^2k, needs only 3 multiplications: ac, bd, (a-b)(c-d)
#
# 2022-02-12    PV

import math

DIRECT_LEN = 4


def ns_compare(n1: str, n2: str) -> int:
    '''Number in string compare: 0 if n1==n2, 1 if n1>n2, -1 if n1<n2'''
    if n1[0] == '-':
        n1 = n1[1:]
        s1 = '-'
    else:
        s1 = '+'

    if n2[0] == '-':
        n2 = n2[1:]
        s2 = '-'
    else:
        s2 = '+'

    # Special case for 0 since we don't care about sign
    if n1 == '0' and n2 == '0':
        return 0

    # If opposite signs, don't care about values to return result
    if s1 == '+' and s2 == '-':
        return 1
    if s1 == '-' and s2 == '+':
        return -1

    # if both are negative, then just swap absolute values
    if s1 == '-' and s2 == '-':
        (n1, n2) = (n2, n1)

    len1 = len(n1)
    len2 = len(n2)
    if len1 > len2:
        return 1
    if len1 < len2:
        return -1
    if n1 == n2:
        return 0
    return 1 if n1 > n2 else -1


# Numeric string addition
def ns_add(n1: str, n2: str) -> str:
    '''Number in string addition, return n1+n2'''
    if n1[0] == '-':
        n1 = n1[1:]
        s1 = '-'
    else:
        s1 = ''

    if n2[0] == '-':
        n2 = n2[1:]
        s2 = '-'
    else:
        s2 = ''

    # At this point, n1 and n2 are absolute values, s1 and s2 contains original sign of n1 and n2
    # Because of recursive slicing, n1 or n2 can start with zeroes, we need to remove them because of
    # length-based comparison mechanism used
    if n1.startswith('0'):
        n1 = n1.lstrip('0')
        if n1 == '':
            n1 = '0'
    if n2.startswith('0'):
        n2 = n2.lstrip('0')
        if n2 == '':
            n2 = '0'

    # Special case for 0
    if n1 == '0':
        return s2+n2
    if n2 == '0':
        return s1+n1

    # Decide if we must do an addition (op='+') or a subtraction (op='-')
    # For subtraction (|n1|-|n2|) ensure that |n1|>|n2|, and resneg bool tells if result is negative
    if s1 == '' and s2 == '':
        op = '+'
        resneg = False
    elif s1 == '-' and s2 == '-':
        op = '+'
        resneg = True
    elif s1 == '' and s2 == '-':
        op = '-'
        if ns_compare(n1, n2) < 0:        # For subtraction,
            (n1, n2) = (n2, n1)
            resneg = True
        else:
            resneg = False
    elif s1 == '-' and s2 == '':
        op = '-'
        if ns_compare(n1, n2) < 0:
            (n1, n2) = (n2, n1)
            resneg = False
        else:
            resneg = True

    # Cheat for unitary tests
    if op == '+':
        r = str(int(n1)+int(n2))
    else:
        assert(int(n1) >= int(n2))
        r = str(int(n1)-int(n2))

    return '-'+r if resneg else r


def ns_neg(n: str) -> str:
    '''Returns opposed value of a number in string'''
    if n[0] == '-':
        return n[1:]
    if n == '0':
        return n
    return '-'+n


def ns_split(n: str, k: int) -> tuple[str, str]:
    '''Split a number in string, returning (high remaining digits, k lower digits)'''
    if len(n) > k:
        return n[:-k], n[-k:]
    else:
        return '0', n


def mult_karatsuba(n1: str, n2: str, depth: int = 0) -> str:
    # Find sign of result, remove sign from n1 and n2
    resneg = False
    if n1[0] == '-':
        n1 = n1[1:]
        resneg = not resneg
    if n2[0] == '-':
        n2 = n2[1:]
        resneg = not resneg

    len1 = len(n1)
    len2 = len(n2)

    # If numbers are small enough, use language/processor multiplication
    if len1+len2 <= 2*DIRECT_LEN:
        if n1 == '0' or n2 == '0':
            return '0'
        return ('-' if resneg else '') + str(int(n1)*int(n2))

    k = max(math.ceil(len1/2), math.ceil(len2/2))
    (b, a) = ns_split(n1, k)
    (d, c) = ns_split(n2, k)

    # print('    '*depth+f'__{a=}')
    # print('    '*depth+f'__{b=}')
    # print('    '*depth+f'__{c=}')
    # print('    '*depth+f'__{d=}')

    ac = mult_karatsuba(a, c, depth+1)
    bd = mult_karatsuba(b, d, depth+1)
    # print('    '*depth+f'_{ac=}')
    # print('    '*depth+f'_{bd=}')
    amb = ns_add(a, ns_neg(b))
    cmd = ns_add(c, ns_neg(d))
    # print('    '*depth+f'{amb=}')
    # print('    '*depth+f'{cmd=}')
    m3 = mult_karatsuba(amb, cmd, depth+1)
    # print('    '*depth+f'_{m3=}')
    m3 = ns_add(m3, ns_neg(ac))
    m3 = ns_add(m3, ns_neg(bd))

    if bd != '0':
        bds = bd + '0'*2*k
    else:
        bds = '0'
    if m3 != '0':
        m3s = m3 + '0'*k
    else:
        m3s = '0'

    # print('    '*depth+f'{bds=}')
    # print('    '*depth+f'{m3s=}')
    # print('    '*depth+f'_{ac=}')

    r = ns_add(bds, ns_neg(m3s))
    r = ns_add(r, ac)

    res = ns_neg(r) if resneg else r
    # print('    '*depth+f'{res=}')
    return res


if __name__ == '__main__':
    n1 = '12344235567885'
    n2 = '567885301234423567567'

    # Pb assert
    n1 = '4235567885'
    n2 = '85301234423567567'

    n1 = '057'
    n2 = '-94'

    r1 = mult_karatsuba(n1, n2)
    r2 = str(int(n1)*int(n2))
    print(r1)
    print(r2)
    print('Ok' if r1 == r2 else 'FAIL!')
