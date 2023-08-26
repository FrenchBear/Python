# Example 23-6. model_v5.py: Quantity and NonBlank, concrete Validated subclasses

class Quantity(Validated):
    """a number greater than zero"""

    def validate(self, name, value):
        if value <= 0:
            raise ValueError(f'{name} must be > 0')
        return value

class NonBlank(Validated):
    """a string with at least one non-space character"""

    def validate(self, name, value):
        value = value.strip()
        if not value:
            raise ValueError(f'{name} cannot be blank')
        return value
