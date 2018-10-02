# copy_deepcopy.py
# Learning python
# Exercise on copy and deepcopy
# 2×3  « dup 1 + lastx 2 * * swap drop »
# 2018-10-02    PV


class TreeNode:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = []
        if parent:
            parent.children.append(self)

    def print(self, m1='', m2=''):
        print(m1 + self.name)
        nm1 = m2 + '┣━ '
        nm2 = m2 + '┃  '
        for ix, child in enumerate(self.children):
            if ix == len(self.children)-1:
                nm1 = m2 + '┗━ '
                nm2 = m2 + '   '
            child.print(nm1, nm2)

    def flatprint(self):
        if len(self.children)==0:
            print(f"Block('{self.name}', '{self.parent.name}', '{self.parent.parent.name}')")
        else:
            for child in self.children:
                child.flatprint()


root = TreeNode('unicode')
scripts = TreeNode('scripts', root)
symbols = TreeNode('symbols', root)
european = TreeNode('european scripts', scripts)
latin = TreeNode('latin', european)
greek = TreeNode('greek', european)
cyrillic = TreeNode('cyrillic', european)
middle_eastern = TreeNode('middle eastern scripts', scripts)
hebrew = TreeNode('hebrew', middle_eastern)
arabic = TreeNode('arabic', middle_eastern)
punctuation = TreeNode('punctuation', symbols)
general_punctuation = TreeNode('general punctuation', punctuation)
supplemental_punctuation = TreeNode('supplemental punctuation', punctuation)
numbers = TreeNode('numbers', symbols)
superscripts = TreeNode('superscripts', numbers)
subscripts = TreeNode('subscripts', numbers)
picto = TreeNode('pictographs', symbols)
emoji = TreeNode('emoji', picto)
dingbats = TreeNode('dingbats', picto)
emoticons = TreeNode('emoticons', picto)

root.print()
root.flatprint()

from copy import copy, deepcopy

rsc = copy(root)
rdc = deepcopy(root)

european.name='LATIN'
numbers.name='NUMBERS'

# rsc.print()
# rdc.print()
