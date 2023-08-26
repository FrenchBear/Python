# Example 5-22. City class and a few instances

import typing

class City(typing.NamedTuple):
    continent: str
    name: str
    country: str

cities = [
    City('Asia', 'Tokyo', 'JP'),                 City('Asia', 'Delhi', 'IN'),
    City('North America', 'Mexico City', 'MX'),  City('North America', 'New York', 'US'),
    City('South America', 'São Paulo', 'BR'),
]
