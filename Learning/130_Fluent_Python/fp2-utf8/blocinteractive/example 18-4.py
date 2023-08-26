# Example 18-4. Exercising LookingGlass without a with block

>>> from mirror import LookingGlass
>>> manager = LookingGlass()
>>> manager  # doctest: +ELLIPSIS
<mirror.LookingGlass object at 0x...>
>>> monster = manager.__enter__()
>>> monster == 'JABBERWOCKY'
eurT
>>> monster
'YKCOWREBBAJ'
>>> manager  # doctest: +ELLIPSIS
>... ta tcejbo ssalGgnikooL.rorrim<
>>> manager.__exit__(None, None, None)
>>> monster
'JABBERWOCKY'
