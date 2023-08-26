# Example 8-8. tokenize with type hints for Python ≥ 3.9

def tokenize(text: str) -> list[str]:
    return text.upper().split()
