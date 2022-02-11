# kmp2.py
# Knuth-Morris-Pratt search algorithm
# Search the index of a substring in a string
# Measure performance compared to naive search algorithm (also implemented in pypthon for fair comparison)
# Test a case that is really favorable to KMP algorithm with many restarts using strings only composed of random '0' and '1' 
#
# Code from Programmation Efficace
#
# 2022-02-11    PV

from random import randint

def kmp2(s, t):
    res = []
    len_s = len(s)
    len_t = len(t)
    r = [0] * len_t
    j = r[0] = -1
    for i in range(1, len_t):
        while j>=0 and t[i-1]!=t[j]:
            j = r[j]
        j+=1
        r[i] = j
    j=0
    for i in range(len_s):
        while j>=0 and s[i]!=t[j]:
            j = r[j]
        j+=1
        if j==len_t:
            #print('Found at', i-len_t+1)
            res.append(i-len_t+1)
            j = r[j-1]+1
    return res

def naive_search(txt: str, pat: str) -> list[int]:
    res = []
    len_txt = len(txt)
    len_pat = len(pat)
    for i in range(len_txt-len_pat):
        for j in range(len_pat):
            if txt[i+j]!=pat[j]:
                break
        else:
            res.append(i)
    return res

'''
txt = 'AAAAABAAAAAB'
pat = 'AAAA'
print(kmp2(txt, pat))
print(naive_search(txt, pat))
breakpoint()
'''


def binary_string(l: int) -> str:
    return ''.join([str(randint(0,1)) for _ in range(l)])

import timeit

def kmp_time():
    SETUP_CODE = '''
from __main__ import kmp2, binary_string
from random import randint

txt = binary_string(10000)
pat = binary_string(10)
def test_kmp():
    l = len(kmp2(txt, pat))
'''
 
    TEST_CODE = '''
test_kmp()
'''
    times = timeit.repeat(setup = SETUP_CODE,
                          stmt = TEST_CODE,
                          repeat = 3,
                          number = 100)
 
    print('kmp:', times)

def naive_time():
    SETUP_CODE = '''
from __main__ import naive_search, binary_string
from random import randint

txt = binary_string(10000)
pat = binary_string(10)
def test_naive():
    l = len(naive_search(txt, pat))
'''
 
    TEST_CODE = '''
test_naive()
'''
    times = timeit.repeat(setup = SETUP_CODE,
                          stmt = TEST_CODE,
                          repeat = 3,
                          number = 100)
 
    print('naive:', times)

kmp_time()
naive_time()
