# testmock.py
# Leaning python, variations on print mocking
# Need much more work to undertand mocking
# https://docs.python.org/3/library/unittest.mock.html
# https://docs.python.org/3/library/unittest.mock-examples.html
#
# 2019-08-28    PV

from unittest.mock import patch, MagicMock

def greet(name):
    print(f'Hello, {name}!')

mock = MagicMock()
@patch('builtins.print', mock)
def test_greet(mock_print):
    greet('Pierre')
    mock_print.assert_called_with('Hello, Pierre!')

test_greet(mock)

