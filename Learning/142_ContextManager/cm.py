# contextmanager.py
# Simple play with a context manager
# Idea while reading "Python tricks"
#
# 2024-11-03    PV      First version

class Indenter:
    def __init__(self):
        self.offset = 0

    def __enter__ (self):
        self.offset += 1
        return self

    def __exit__ (self, exc_type, exc_value, exc_tb):
        self.offset -= 1

    def print(self, msg):
        print('    '*(self.offset-1), msg, sep='')


with Indenter() as indent:
    indent.print('hi!')
    with indent:
        indent.print('hello')
        with indent:
            indent.print('bonjour')
    indent.print('hey')
