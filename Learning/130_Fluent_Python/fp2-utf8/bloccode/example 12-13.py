# Example 12-13. The Vector.__eq__ implementation using zip in a for loop for more efficient comparison

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for a, b in zip(self, other):
            if a != b:
                return False
        return True
