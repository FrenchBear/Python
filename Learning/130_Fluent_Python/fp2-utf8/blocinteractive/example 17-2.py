# Example 17-2. Testing iteration on a Sentence instance

>>> s = Sentence('"The time has come," the Walrus said,')
>>> s
Sentence('"The time ha... Walrus said,')
>>> for word in s:
...     print(word, end=' ')
...
The time has come the Walrus said
>>> list(s)
['The', 'time', 'has', 'come', 'the', 'Walrus', 'said']
