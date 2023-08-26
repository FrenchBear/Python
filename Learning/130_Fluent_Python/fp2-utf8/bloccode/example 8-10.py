# Example 8-10. tokenize with type hints for Python ≥ 3.5

from typing import List

def tokenize(text: str) -> List[str]:
    return text.upper().split()
