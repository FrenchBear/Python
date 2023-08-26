# Example 5-20. dataclass/resource.py: code for Resource, a class based on Dublin Core terms

>>> description = 'Improving the design of existing code'
>>> book = Resource('978-0-13-475759-9', 'Refactoring, 2nd Edition',
...     ['Martin Fowler', 'Kent Beck'], date(2018, 11, 19),
...     ResourceType.BOOK, description, 'EN',
...     ['computer programming', 'OOP'])
>>> book  # doctest: +NORMALIZE_WHITESPACE
Resource(identifier='978-0-13-475759-9', title='Refactoring, 2nd Edition', creators=['Martin Fowler', 'Kent Beck'], date=datetime.date(2018, 11, 19), type=<ResourceType.BOOK: 1>, description='Improving the design of existing code', language='EN', subjects=['computer programming', 'OOP'])
