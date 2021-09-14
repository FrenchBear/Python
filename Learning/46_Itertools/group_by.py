# group_by.py
# Learning python
# More on itertools.groupby, transform a flat list into a hierachical tree
#
# 2018-10-02    PV

from dataclasses import dataclass
from itertools import groupby
from operator import attrgetter


@dataclass
class Block:
    name: str
    l1: str
    l2: str


Blocks = [
    Block('latin', 'european scripts', 'scripts'),
    Block('greek', 'european scripts', 'scripts'),
    Block('cyrillic', 'european scripts', 'scripts'),
    Block('hebrew', 'middle eastern scripts', 'scripts'),
    Block('arabic', 'middle eastern scripts', 'scripts'),
    Block('general punctuation', 'punctuation', 'symbols'),
    Block('supplemental punctuation', 'punctuation', 'symbols'),
    Block('superscripts', 'numbers', 'symbols'),
    Block('subscripts', 'numbers', 'symbols'),
    Block('emoji', 'pictographs', 'symbols'),
    Block('dingbats', 'pictographs', 'symbols'),
    Block('emoticons', 'pictographs', 'symbols'),
]


# Flat list
for block in Blocks:
    print('{l2:10} {l1:25} {name}'.format(l2=block.l2, l1=block.l1, name=block.name))
print()


class TreeNode:
    def __init__(self, name, parent=None):
        if parent and not isinstance(parent, TreeNode):
            raise TypeError("parent must be a TreeNode or None")
        self.name = name
        self.parent = parent
        self.children = []
        if parent:
            parent.children.append(self)

    def print(self, m1='', m2=''):
        print(m1 + self.name)
        nm1 = m2 + '├─ '
        nm2 = m2 + '│  '
        for ix, child in enumerate(self.children):
            if ix == len(self.children)-1:
                nm1 = m2 + '╰─ '
                nm2 = m2 + '   '
            child.print(nm1, nm2)


# Building a tree
root = TreeNode('unicode')
for k2, g2 in groupby(sorted(Blocks, key=attrgetter('l2')), attrgetter('l2')):
    print(k2)
    n2 = TreeNode(k2, root)
    for k1, g1 in groupby(sorted(g2, key=attrgetter('l1')), attrgetter('l1')):
        print('  '+k1)
        n1 = TreeNode(k1, n2)
        for k0, g0 in groupby(sorted(g1, key=attrgetter('name')), attrgetter('name')):
            print('    '+k0)
            TreeNode(k0, n1)


# Print hierarchical tree
print()
root.print()
