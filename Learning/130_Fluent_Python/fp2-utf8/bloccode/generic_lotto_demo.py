# Example 15-15. generic_lotto_demo.py: using a generic lottery blower class

from generic_lotto import LottoBlower

machine = LottoBlower[int](range(1, 11))

first = machine.pick()
remain = machine.inspect()
