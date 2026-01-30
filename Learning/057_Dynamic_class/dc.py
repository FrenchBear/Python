class DynaClass:
    def __init__(self, *args, **kwargs):
        pass

    def __getattribute__(self, name):
        return '<'+name+'>'

dc = DynaClass()
print(dc.pomme)
print(dc.poire)

