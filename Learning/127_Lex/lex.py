# Lex
# Efficient tokenizer
#
# 2023-04-10    PV      First version

import time
from roman import *

init_roman()

# Simple quick test
s = "MCMLXV"
print(f"{s} = {RomanToInt(s)}")
d = 1965
print(f"{d} = {IntToRoman(d)}")

t: float = time.perf_counter_ns()
for i in range(1_000_000):
    assert RomanToInt(IntToRoman(i))==i
t = (time.perf_counter_ns()-t)/1_000_000_000
print(f'Duration: {int(t)}.{int(1000*t)%1000:0>3} s')
