# Example 29-2. Cheese has a kind attribute and a standard representation

class Cheese:

    def __init__(self, kind):
        self.kind = kind

    def __repr__(self):
        return f'Cheese({self.kind!r})'
