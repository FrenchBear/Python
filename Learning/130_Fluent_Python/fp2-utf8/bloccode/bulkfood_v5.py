# Example 23-7. bulkfood_v5.py: LineItem using Quantity and NonBlank descriptors

import model_v5 as model

class LineItem:
    description = model.NonBlank()
    weight = model.Quantity()
    price = model.Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price
