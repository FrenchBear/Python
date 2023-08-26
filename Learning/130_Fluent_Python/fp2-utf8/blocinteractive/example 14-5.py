# Example 14-5. Doctests for calling ping and pong on a Leaf object

>>> leaf1 = Leaf()
>>> leaf1.ping()
<instance of Leaf>.ping() in Leaf
<instance of Leaf>.ping() in A
<instance of Leaf>.ping() in B
<instance of Leaf>.ping() in Root

>>> leaf1.pong()
<instance of Leaf>.pong() in A
<instance of Leaf>.pong() in B
