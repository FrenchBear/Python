# Example 9-10. Inspecting the function created by make_averager in Example 9-8

>>> avg.__code__.co_varnames
('new_value', 'total')
>>> avg.__code__.co_freevars
('series',)
