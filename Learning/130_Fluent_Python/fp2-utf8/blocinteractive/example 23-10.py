# Example 23-10. Overriding descriptor without __get__

>>> obj.over_no_get
<__main__.OverridingNoGet object at 0x665bcc>
>>> Managed.over_no_get
<__main__.OverridingNoGet object at 0x665bcc>
>>> obj.over_no_get = 7
-> OverridingNoGet.__set__(<OverridingNoGet object>, <Managed object>, 7)
>>> obj.over_no_get
<__main__.OverridingNoGet object at 0x665bcc>
>>> obj.__dict__['over_no_get'] = 9
>>> obj.over_no_get
9
>>> obj.over_no_get = 7
-> OverridingNoGet.__set__(<OverridingNoGet object>, <Managed object>, 7)
>>> obj.over_no_get
9
