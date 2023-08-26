# Example 22-20. A negative weight results in a negative subtotal

>>> raisins = LineItem('Golden raisins', 10, 6.95)
>>> raisins.subtotal()
69.5
>>> raisins.weight = -20  # garbage in...
>>> raisins.subtotal()    # garbage out...
-139.0
