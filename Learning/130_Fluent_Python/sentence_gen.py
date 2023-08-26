# Example 17-5

import re
import reprlib

RE_WORD = re.compile(r'\w+')

class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        for word in self.words:
            yield word
# done!

s = Sentence('"The time has come," the Walrus said,')
print(s)
for word in s:
    print(word, end=' ')
print()
print(list(s))
