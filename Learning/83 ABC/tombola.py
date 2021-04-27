# tombola.py
# ABC example, from Fluent Python
# 2021-04-27    PV

import abc

class Tombola(abc.ABC):

    @abc.abstractmethod
    def load(self, iterable):
        """Add items from an iterable."""
    
    @abc.abstractmethod
    def pick(self):
        """Remove item at random, returning it.  Raise LookupError when the instance is empty."""

    def loaded(self):
        """Returns True it there is at least one item."""
        return bool(self.inspect())

    def inspect(self):
        """Returns a sorted tuple of the current items."""
        items = []
        while True:
            try:
                items.append(self.pick())
            except LookupError:
                break
            self.load(items)
            return tuple(sorted(items))


