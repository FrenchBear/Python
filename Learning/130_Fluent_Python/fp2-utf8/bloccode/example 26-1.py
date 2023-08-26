# Example 26-1. Search for needles in haystack and count those found

found = 0
for n in needles:
    if n in haystack:
        found += 1
