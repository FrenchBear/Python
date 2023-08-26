# Example 4-8. A platform encoding issue (if you try this on your machine, you may or may not see the problem)

>>> open('cafe.txt', 'w', encoding='utf_8').write('café')
4
>>> open('cafe.txt').read()
'cafÃ©'
