# Example 11-5. Vector2d.__format__ method, take #1

    # inside the Vector2d class

    def __format__(self, fmt_spec=''):
        components = (format(c, fmt_spec) for c in self)
        return '({}, {})'.format(*components)
