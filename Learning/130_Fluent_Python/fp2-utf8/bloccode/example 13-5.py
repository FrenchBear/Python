# Example 13-5. Duck typing to handle a string or an iterable of strings

    try:
        field_names = field_names.replace(',', ' ').split()
    except AttributeError:
        pass
    field_names = tuple(field_names)
    if not all(s.isidentifier() for s in field_names):
        raise ValueError('field_names must all be valid identifiers')
