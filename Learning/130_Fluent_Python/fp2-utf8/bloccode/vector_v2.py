# Example 12-6. Part of vector_v2.py: __len__ and __getitem__ methods added to Vector class from vector_v1.py (see Example 12-2)

    def __len__(self):
        return len(self._components)

    def __getitem__(self, key):
        if isinstance(key, slice):
            cls = type(self)
            return cls(self._components[key])
        index = operator.index(key)
        return self._components[index]
