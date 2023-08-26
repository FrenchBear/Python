# Example 22-29. bulkfood_v2prop.py: exploring properties and storage attributes

>>> nutmeg = LineItem('Moluccan nutmeg', 8, 13.95)
>>> nutmeg.weight, nutmeg.price
(8, 13.95)
>>> nutmeg.__dict__
{'description': 'Moluccan nutmeg', 'weight': 8, 'price': 13.95}
