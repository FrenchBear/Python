# Example 3-13. Count occurrences of needles in a haystack (same end result as Example 3-12)

found = 0
for n in needles:
    if n in haystack:
        found += 1
