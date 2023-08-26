# Example 15-9. books_any.py: from_json function

def from_json(data: str) -> BookDict:
    whatever = json.loads(data)
    return whatever
