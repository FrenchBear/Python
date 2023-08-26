class Vector:
    # many lines omitted

    def __eq__(self, other):
        return (len(self) == len(other) and all(a == b for a, b in zip(self, other)))
