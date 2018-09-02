# Context Manager
# 2018-09-02    PV


class Indenter():
    level = 0

    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self):
        Indenter.level += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        Indenter.level -= 1

    def print(self, *s):
        print('  '*(Indenter.level-1), end='')
        print(*s)


with Indenter() as indent:
    indent.print('hi!')
    with indent:
        indent.print('hello')
        with indent:
            indent.print('bonjour')
    indent.print('hey')

