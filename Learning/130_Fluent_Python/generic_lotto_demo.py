# Example 15-15

from generic_lotto import LottoBlower

machine = LottoBlower[int](range(1, 11))

first = machine.pick()
remain = machine.inspect()
