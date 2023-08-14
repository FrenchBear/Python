# Example 15-6

def demo() -> None:
    book = BookDict(
        isbn='0134757599',
        title='Refactoring, 2e',
        authors=['Martin Fowler', 'Kent Beck'],
        pagecount=478
    )
    authors = book['authors']
    if TYPE_CHECKING:
        reveal_type(authors)
    authors = 'Bob'
    book['weight'] = 4.2
    del book['title']

if __name__ == '__main__':
    demo()
