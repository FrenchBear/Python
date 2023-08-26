# Example 8-9. tokenize with type hints for Python ≥ 3.7

from __future__ import annotations

def tokenize(text: str) -> list[str]:
    return text.upper().split()
