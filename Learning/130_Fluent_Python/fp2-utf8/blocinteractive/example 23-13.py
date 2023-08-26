# Example 23-13. A method is a non-overriding descriptor

>>> obj = Managed()
>>> obj.spam
<bound method Managed.spam of <descriptorkinds.Managed object at 0x74c80c>>
>>> Managed.spam
<function Managed.spam at 0x734734>
>>> obj.spam = 7
>>> obj.spam
7
