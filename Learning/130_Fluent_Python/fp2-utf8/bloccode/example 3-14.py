# Example 3-14. Count occurrences of needles in a haystack; these lines work for any iterable types

found = len(set(needles) & set(haystack))
# another way:
found = len(set(needles).intersection(haystack))
