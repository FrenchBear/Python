# Example 23-12. Any descriptor can be overwritten on the class itself

>>> obj = Managed()
>>> Managed.over = 1
>>> Managed.over_no_get = 2
>>> Managed.non_over = 3
>>> obj.over, obj.over_no_get, obj.non_over
(1, 2, 3)
