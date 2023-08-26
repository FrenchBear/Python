# Example 5-12. meaning/demo_dc.py: a class decorated with @dataclass

from dataclasses import dataclass

@dataclass
class DemoDataClass:
    a: int
    b: float = 1.1
    c = 'spam'
