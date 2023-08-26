# Example 15-10. books.py: from_json function with variable annotation

def from_json(data: str) -> BookDict:
    whatever: BookDict = json.loads(data)
    return whatever
