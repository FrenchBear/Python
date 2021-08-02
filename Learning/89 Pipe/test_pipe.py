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
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).pipe_where(lambda a: a.startswith('c'))
        self.assertEqual(list(p), ['chien', 'chat'])

    def test_where_2(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).pipe_where(lambda a: a.startswith('z'))
        self.assertEqual(list(p), [])

    # select transformation
    def test_select_1(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).pipe_select(lambda a: len(a))
        self.assertEqual(list(p), [5, 4, 4, 3, 4, 5])

    # first selection
    def test_first_1(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).pipe_first()
        self.assertEqual(list(p), ['chien'])

    def test_first_2(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).pipe_first(lambda a: a.startswith('o'))
        self.assertEqual(list(p), ['ours'])

    def test_first_3(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).pipe_first(lambda a: a.startswith('z'))
        self.assertEqual(list(p), [])

    def test_first_4(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).final_first_or_none()
        self.assertEqual(p, 'chien')

    def test_first_5(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).final_first_or_none(lambda a: a.startswith('r'))
        self.assertEqual(p, 'rat')

    def test_first_6(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).final_first_or_none(lambda a: len(a) == 20)
        self.assertEqual(p, None)

    # count elements
    def test_count_1(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).final_count()
        self.assertEqual(p, 6)

    def test_count_2(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).final_count(lambda a: len(a) == 4)
        self.assertEqual(p, 3)

    # sum elements
    def test_sum_1(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).pipe_select(lambda a: len(a)).final_sum()
        self.assertEqual(p, 25)

    def test_sum_2(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).pipe_select(lambda a: len(a)).final_sum(lambda a: a > 4)
        self.assertEqual(p, 10)

    # sort elements
    def test_sort_1(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).pipe_sort()
        self.assertEqual(list(p), ['boeuf', 'chat', 'chien', 'ours', 'porc', 'rat'])

    def test_sort_2(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).pipe_sort(reverse=True)
        self.assertEqual(list(p), ['rat','porc','ours','chien','chat','boeuf'])

    def test_sort_3(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).pipe_sort(lambda a: len(a))
        self.assertEqual(list(p), ['rat','chat','ours','porc','chien','boeuf'])

    def test_sort_2(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).pipe_sort(lambda a: len(a), True)
        self.assertEqual(list(p), ['chien','boeuf','chat','ours','porc','rat'])

    # reverse elements
    def test_reverse_1(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).pipe_reverse()
        self.assertEqual(list(p), ['boeuf','porc','rat','ours','chat','chien'])



if __name__ == '__main__':
    unittest.main()
