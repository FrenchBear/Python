# slice_explorer.py
# Just show how [] works
#
# 2023-08-05    PV

class MySeq:
    def __getitem__(self, index):
        return index


s = MySeq()
print(s[1])
print(s['Hello'])
print(s[3.1416])
print(s[3 + 2j])
print(s[None])
print(s[...])
print(s[MySeq()])
print(s[[1,2]])
print(s[{'one':1, 'two':2}])
print(s[object()])

print()
print(s[1:2])
print(s[1:])
print(s[:2])
print(s[::-1])
print(s['a':'b':2j])        # type: ignore
print(s[1:2:3])
print(s[:])
print(s[...:None:1.414])    # type: ignore

print()
print(s[1,2])
print(s[((1,2))])
print(s['a',None,-1,7])
print(s[1:2:3, 3:2, :, ...])
