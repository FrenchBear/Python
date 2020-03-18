from collections import defaultdict

class DefaultDictList(dict): 
    def __missing__(self, key):
        value = list()
        self[key] = value 
        return value

ndg = DefaultDictList()
#ndg = defaultdict(list)
nds = ndg['pomme']
nds.append('Joe')
