# Dictionaries
# Learning Python
#
# 2015-05-02    PV
# 2018-08-24    PV      More code
# 2018-09-10    PV      collections.OrderedDict, collections.ChainMap, types.MappingProxyType


from types import MappingProxyType
from typing import DefaultDict
import collections

dic = {"Pierre": 50, "Claude": 59, "Jacques": 46}

print(dic)
print(dic.values())  # View, wrap into list() to make a list
print(dic.keys())  # Idem
print(list(dic))  # ['Claude', 'Pierre', 'Jacques'] = keys

# Access by index
# print(dic[0])                 # Invalid
print(
    list(dic.values())[0]
)  # Working, but since dictionaries don't keep order, element 0 is Claude!

dic["Pierre"] += 1  # Dictionaries are mutable
print(dic["Pierre"])

# print(dic['pierre'])          # Err, case-sensitive

print(len(dic))  # 3

del dic["Jacques"]
print(dic)  # {'Claude': 59, 'Pierre': 51}

print("Pierre" in dic)  # True
print("Jacques" in dic)  # False

print(dic.get("Pierre", 20))  # 51
print(dic.get("Jacques", 20))  # 20
try:
    print(dic["jacques"])
except Exception:
    print("exception: 20")

dic.clear()
print(len(dic))  # 0

# Use a dictionary as a sparse matrix, key is a tuple
Matrix = {}
Matrix[1, 2] = 15
print(Matrix[1, 2])
print(Matrix)  # {(1, 2): 15}

"""
Interfaces d=dict, dd=defaultdict, od=OrderedDict
                            d   dd  od
d.clear()	                x	x	x 	Remove all items
d.__contains__(k)	        x	x	x 	k in d
d.copy()	                x	x	x 	Shallow copy
d.__copy__()	                x		Support for copy.copy
d.default_factory	            x		Callable invoked by __missing__ to set missing values
d.__delitem__(k)	        x	x	x 	del d[k] —— remove item with key k
d.fromkeys(it, [initial])	x	x	x 	New mapping from keys in iterable, with optional initial value (defaults to None)
d.get(k, [default])	        x	x	x 	Get item with key k, return default or None if missing
d.__getitem__(k)	        x	x	x 	d[k] —— get item with key k
d.items()	                x	x	x 	Get view over items —— (key, value) pairs
d.__iter__()	            x	x	x 	Get iterator over keys
d.keys()                	x	x	x 	Get view over keys
d.__len__()	                x	x	x 	len(d) —— number of items
d.__missing__(k)                x 		Called when __getitem__ cannot find the key
d.move_to_end(k, [last])	        x	Move k first or last position (last is True by default)
d.pop(k, [default])         x	x	x 	Remove and return value at k, or default or None if missing
d.popitem()	                x	x	x 	Remove and return an arbitrary (key, value) item (default: first inserted, FIFO, but with True arg, pops last inserted, LIFO)
d.__reversed__()	                x	Get iterator for keys from last to first inserted
d.setdefault(k, [default])	x	x	x 	If k in d, return d[k]; else set d[k]=default and return it
d.__setitem__(k, v)	        x	x	x 	d[k]=v —— put v at k
d.update(m, [**kargs])	    x	x	x 	Update d with items from mapping or iterable of(key, value) pairs
d.values()	                x	x	x 	Get view over values
"""

# defaultdict: when instantiating a defaultdict, you provide a callable that is
# used to produce a default value whenever __getitem__ is passed a nonexistent key argument.

print("\ndefaultdict")
dd: DefaultDict[str, str] = collections.defaultdict(str)
dd["color"] += "Red"
dd["size"] += "Small"
dd["color"] += ", Blue"
dd["size"] += ", Big"
print(dd)

dd2 = collections.defaultdict(list)  # use list constructor as default_factory
dd2[1].append("Un")
dd2[1].append("One")
dd2[1].append("Eins")
dd2[2].append("Deux")
print(dd2)

# collections.OrderedDict, remember order of insertion of the keys
print("\nOrderedDict")
od = collections.OrderedDict(one=1, two=2, three=3)
print(od)
od["four"] = 4
print(od.keys())
od.popitem(True)  # Remove last inserted
print(od.keys())

# collections.ChainMap; serch multiple dictionaries
print("\nChainMap")
dict1 = {"one": 1, "two": 2}
dict2 = {"three": 3, "four": 4}
chain = collections.ChainMap(dict1, dict2)
print("'one' in chain:", "one" in chain)
print("'three' in chain:", "three" in chain)
print("'five' in chain:", "five" in chain)

# types.MappingProxyType – A wrapper for making read-only dictionaries
writable = {"one": 1, "two": 2}
read_only = MappingProxyType(writable)
writable["one"] = 42
print(read_only)
# read_only['two'] = 4          # Error: 'mappingproxy' object does not support item assignment
