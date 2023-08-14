# Example 15-16

from generic_lotto import LottoBlower

machine = LottoBlower[int]([1, .2])
## error: List item 1 has incompatible type "float";
##        expected "int"

machine = LottoBlower[int](range(1, 11))

machine.load('ABC')
