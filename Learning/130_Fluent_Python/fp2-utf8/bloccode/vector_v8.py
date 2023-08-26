# Example 16-14. vector_v8.py: improved __eq__ in the Vector class

    def __eq__(self, other):
        if isinstance(other, Vector):
            return (len(self) == len(other) and all(a == b for a, b in zip(self, other)))
        else:
            return NotImplemented
