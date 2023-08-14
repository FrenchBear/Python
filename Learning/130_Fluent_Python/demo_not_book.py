# Example 15-11

from books import to_xml, from_json
from typing import TYPE_CHECKING

def demo() -> None:
    NOT_BOOK_JSON = """
        { "title": "Andromeda Strain",
          "flavor": "pistachio",
          "authors": true }
    """
    not_book = from_json(NOT_BOOK_JSON)
    if TYPE_CHECKING:
        reveal_type(not_book)
        reveal_type(not_book['authors'])
    print(not_book)
    print(not_book['flavor'])
    xml = to_xml(not_book)
    print(xml)

if __name__ == '__main__':
    demo()
