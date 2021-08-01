# test_pipe.py
# Units tests for Pipe class
# 2021-08-02    PV

from pipe import Pipe
import unittest


class TestPipe(unittest.TestCase):

    # A Pipe(it) is iterable and iterates over argument it 
    def test_pipe_1(self):
        p = Pipe([1, 2, 3])
        self.assertEqual(list(p), [1, 2, 3])

    # Calling Pipe() with non-iterable arg raises a TypeError
    def test_pipe_2(self):
        self.assertRaises(TypeError, Pipe, 23)

    # where filtering
    def test_where_1(self):
        animaux = ['chien', 'chat', 'ours', 'âne', 'porc', 'boeuf']
        p = Pipe(animaux).pipe_where(lambda a: a.startswith('c'))
        self.assertEqual(list(p), ['chien', 'chat'])

    def test_where_2(self):
        animaux = ['chien', 'chat', 'ours', 'âne', 'porc', 'boeuf']
        p = Pipe(animaux).pipe_where(lambda a: a.startswith('z'))
        self.assertEqual(list(p), [])

    # select transformation
    def test_select_1(self):
        animaux = ['chien', 'chat', 'ours', 'âne', 'porc', 'boeuf']
        p = Pipe(animaux).pipe_select(lambda a: len(a))
        self.assertEqual(list(p), [5, 4, 4, 3, 4, 5])


if __name__ == '__main__':
    unittest.main()
