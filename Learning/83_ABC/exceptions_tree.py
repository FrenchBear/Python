# exceptions_tree.py
# Print tree of Python standard exceptions
# 2021-05-01    PV

def tree(cls: type, margin: str) -> None:
    ns = len(cls.__subclasses__())
    for i,sc in enumerate(cls.__subclasses__()):
        print(margin+('└──' if i==ns-1 else '├──')+' '+sc.__name__)
        tree(sc, margin+'    ' if i==ns-1 else margin+'|   ')

print('Exception')
tree(Exception, '')
