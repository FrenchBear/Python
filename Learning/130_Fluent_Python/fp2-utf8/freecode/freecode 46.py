def test_irregular() -> None:
    got = show_count(2, 'child', 'children')
    assert got == '2 children'
