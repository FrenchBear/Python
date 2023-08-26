# Example 12-14. The Vector.__eq__ implementation using zip and all: same logic as Example 12-13

    def __eq__(self, other):
        return len(self) == len(other) and all(a == b for a, b in zip(self, other))
