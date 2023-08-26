# Example 10-7. The promos list is built by introspection of the module global namespace

from decimal import Decimal
from strategy import Order
from strategy import (fidelity_promo, bulk_item_promo, large_order_promo)

promos = [promo for name, promo in globals().items()
                if name.endswith('_promo') and
                   name != 'best_promo'
]
def best_promo(order: Order) -> Decimal:
    """Compute the best discount available"""
    return max(promo(order) for promo in promos)
