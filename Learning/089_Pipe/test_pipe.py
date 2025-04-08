# test_pipe.py
# Units tests for Pipe class
#
# 2021-08-02    PV

from pipe import Pipe
import unittest


class TestPipe(unittest.TestCase):

    # A Pipe(it) is iterable and iterates over argument it
    def test_1(self):
        p = Pipe([1, 2, 3])
        self.assertEqual(list(p), [1, 2, 3])

    # Calling Pipe() with non-iterable arg raises a TypeError
    def test_2(self):
        self.assertRaises(TypeError, Pipe, 23)

    # where filtering
    def test_where_1(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).where(lambda a: a.startswith('c'))
        self.assertEqual(list(p), ['chien', 'chat'])

    def test_where_2(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).where(lambda a: a.startswith('z'))
        self.assertEqual(list(p), [])

    # select transformation
    def test_select_1(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).select(lambda a: len(a))
        self.assertEqual(list(p), [5, 4, 4, 3, 4, 5])

    # select first
    def test_first_1(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).first_or_none()
        self.assertEqual(p, 'chien')

    def test_first_2(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).first_or_none(lambda a: a.startswith('r'))
        self.assertEqual(p, 'rat')

    def test_first_3(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).first_or_none(lambda a: len(a) == 20)
        self.assertEqual(p, None)

    # select last
    def test_last_1(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).last_or_none()
        self.assertEqual(p, 'boeuf')

    def test_last_2(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).last_or_none(lambda a: a.startswith('c'))
        self.assertEqual(p, 'chat')

    def test_last_3(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).last_or_none(lambda a: len(a) == 20)
        self.assertEqual(p, None)

    # count elements
    def test_count_1(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).count()
        self.assertEqual(p, 6)

    def test_count_2(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).count(lambda a: len(a) == 4)
        self.assertEqual(p, 3)

    # sum elements
    def test_sum_1(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).select(lambda a: len(a)).sum()
        self.assertEqual(p, 25)

    def test_sum_2(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).select(lambda a: len(a)).sum(lambda a: a > 4)
        self.assertEqual(p, 10)

    def test_sum_3(self):
        p = Pipe(range(1, 10, 2)).sum()
        self.assertEqual(p, 25)     # 25 = 1+3+5+7+9

    # Min
    def test_min_1(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).min()
        self.assertEqual(p, 'boeuf')

    def test_min_2(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).min(lambda a: len(a)==4)
        self.assertEqual(p, 'chat')

    # Max
    def test_max_1(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).max()
        self.assertEqual(p, 'rat')

    def test_max_2(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).max(lambda a: len(a)==4)
        self.assertEqual(p, 'porc')

    # sort elements
    def test_sort_1(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).sort()
        self.assertEqual(list(p), ['boeuf', 'chat', 'chien', 'ours', 'porc', 'rat'])

    def test_sort_2(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).sort(reverse=True)
        self.assertEqual(list(p), ['rat', 'porc', 'ours', 'chien', 'chat', 'boeuf'])

    def test_sort_3(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).sort(lambda a: len(a))
        self.assertEqual(list(p), ['rat', 'chat', 'ours', 'porc', 'chien', 'boeuf'])

    def test_sort_4(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).sort(lambda a: len(a), True)
        self.assertEqual(list(p), ['chien', 'boeuf', 'chat', 'ours', 'porc', 'rat'])

    # reverse elements
    def test_reverse(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).reverse()
        self.assertEqual(list(p), ['boeuf', 'porc', 'rat', 'ours', 'chat', 'chien'])

    # contat iterables
    def test_concat(self):
        animaux = ['chien', 'chat', 'ours']
        fruits = ['pomme', 'poire', 'ananas']
        couleurs = ['bleu', 'blanc', 'rouge']
        p = Pipe(animaux).concat(fruits, couleurs)
        self.assertEqual(list(p), ['chien', 'chat', 'ours', 'pomme', 'poire', 'ananas', 'bleu', 'blanc', 'rouge'])

    # join elements
    def test_join(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).join(',')
        self.assertEqual(p, 'chien,chat,ours,rat,porc,boeuf')

    # range generator
    def test_range(self):
        self.assertEqual(list(Pipe.range(10)), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(list(Pipe.range(1, 10)), [1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(list(Pipe.range(1, 10, 2)), [1, 3, 5, 7, 9])

    # test any()
    def test_any(self):
        self.assertEqual(Pipe([]).any(), False)
        self.assertEqual(Pipe([1, 2, 3]).any(), True)
        self.assertEqual(Pipe([1, 2, 3]).any(lambda a: a == 2), True)
        self.assertEqual(Pipe([1, 2, 3]).any(lambda a: a == 5), False)

    # test all()
    def test_all(self):
        self.assertEqual(Pipe.range(5).all(lambda x: x >= 0), True)
        self.assertEqual(Pipe.range(5).all(lambda x: x >= 6), False)

    # test contains()
    def test_contains(self):
        fruits = ['pomme', 'poire', 'ananas']
        self.assertEqual(Pipe.range(5).contains(9), False)
        self.assertEqual(Pipe(fruits).contains('poire'), True)

    # test distinct()
    def test_distinct(self):
        p = Pipe('mississippi').distinct().sort()
        self.assertEqual(list(p), ['i', 'm', 'p', 's'])

    # test intersect()
    def test_intersect(self):
        p = Pipe.range(0, 100, 2).intersect(Pipe.range(0, 100, 3), Pipe.range(0, 100, 5)).sort()
        self.assertEqual(list(p), [0, 30, 60, 90])
    
    # test union()
    def test_union(self):
        p = Pipe('asterix').union(Pipe('obelix')).sort()
        self.assertEqual(list(p), ['a','b','e','i','l','o','r','s','t','x'])

    # test repeat()
    def test_repeat(self):
        p = Pipe.repeat('yes!', 3)
        self.assertEqual(list(p), ['yes!', 'yes!', 'yes!'])
        p = Pipe.repeat(1, 6)
        self.assertEqual(list(p), [1, 1, 1, 1, 1, 1])

    # test_skip()
    def test_skip(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).skip(2)
        self.assertEqual(list(p), ['ours','rat','porc','boeuf'])

    # test skip_last()
    def test_skip_last(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).skip_last(2)
        self.assertEqual(list(p), ['chien', 'chat', 'ours', 'rat'])

    # test take()
    def test_take(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).take(2)
        self.assertEqual(list(p), ['chien', 'chat'])

    # test take_last()
    def test_take_last(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).take_last(2)
        self.assertEqual(list(p), ['porc', 'boeuf'])
    
    # test skip_while()
    def test_take_while(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).take_while(lambda a: a!='ours')
        self.assertEqual(list(p), ['chien', 'chat'])

    # test skip_while()
    def test_skip_while(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).skip_while(lambda a: a!='ours')
        self.assertEqual(list(p), ['ours','rat','porc','boeuf'])

    # test zip()
    def test_zip(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        fruits = ['pomme', 'poire', 'ananas']
        couleurs = ['bleu', 'blanc', 'rouge']
        p = Pipe(animaux).zip(fruits, couleurs)
        self.assertEqual(list(p), [('chien', 'pomme', 'bleu'),('chat', 'poire', 'blanc'),('ours', 'ananas', 'rouge')])

    # test append()
    def test_append(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).append('lion')
        self.assertEqual(list(p), ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf', 'lion'])

    # test prepend()
    def test_prepend(self):
        animaux = ['chien', 'chat', 'ours', 'rat', 'porc', 'boeuf']
        p = Pipe(animaux).prepend('lion')
        self.assertEqual(list(p), ['lion', 'chien', 'chat', 'ours', 'rat', 'porc', 'boeuf'])



if __name__ == '__main__':
    unittest.main()
