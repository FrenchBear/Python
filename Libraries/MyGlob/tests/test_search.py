# MyGlob tests - test_search
# Unit tests for MyGlob
#
# 2025-09-10    PV
# 2025-09-13    PV      Added test_search_error_2

import unittest
import sys
import os
import shutil
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from myglob import MyGlobBuilder, MyGlobError

class TestSearch(unittest.TestCase):

    def setUp(self):
        self.test_dir = Path("C:/Temp/search1_py")
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        self.test_dir.mkdir(parents=True, exist_ok=True)

        (self.test_dir / "fruits et légumes.txt").write_text("Des fruits et des légumes", encoding='utf-8')
        (self.test_dir / "info").write_text("Information", encoding='utf-8')
        
        fruits_dir = self.test_dir / "fruits"
        fruits_dir.mkdir()
        (fruits_dir / "pomme.txt").write_text("Pomme", encoding='utf-8')
        (fruits_dir / "poire.txt").write_text("Poire", encoding='utf-8')
        (fruits_dir / "ananas.txt").write_text("Ananas", encoding='utf-8')
        (fruits_dir / "tomate.txt").write_text("Tomate", encoding='utf-8')

        legumes_dir = self.test_dir / "légumes"
        legumes_dir.mkdir()
        (legumes_dir / "épinard.txt").write_text("Épinard", encoding='utf-8')
        (legumes_dir / "tomate.txt").write_text("Tomate", encoding='utf-8')
        (legumes_dir / "pomme.de.terre.txt").write_text("Pomme de terre", encoding='utf-8')

        chinese_dir = self.test_dir / "我爱你"
        chinese_dir.mkdir()
        (chinese_dir / "你好世界.txt").write_text("Hello world", encoding='utf-8')
        (chinese_dir / "tomate.txt").write_text("Hello Tomate", encoding='utf-8')

        deep_dir = chinese_dir / "Ƥḭҽɾɾҽ ѵìǫłҽղէ"
        deep_dir.mkdir()
        (deep_dir / "tomate.txt").write_text("Hello Tomate", encoding='utf-8')
        (deep_dir / "Aé♫山𝄞🐗.txt").write_text("Random 1", encoding='utf-8')
        (deep_dir / "œæĳøß≤≠Ⅷﬁﬆ.txt").write_text("Random 2", encoding='utf-8')

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def search_count_base(self, builder):
        nf = 0
        nd = 0
        try:
            gs = builder.compile()
            for ma in gs.explore():
                if ma.error:
                    print(ma.error)
                    continue
                if ma.is_file:
                    nf += 1
                elif ma.is_dir:
                    nd += 1
        except MyGlobError as e:
            self.fail(f"MyGlobError raised: {e}")
        return (nf, nd)

    def search_count(self, glob_pattern):
        return self.search_count_base(MyGlobBuilder(glob_pattern))

    def search_count_autorecurse(self, glob_pattern):
        return self.search_count_base(MyGlobBuilder(glob_pattern).set_autorecurse(True))

    def search_count_ignore(self, glob_pattern, ignore_dirs):
        builder = MyGlobBuilder(glob_pattern)
        for ignore_dir in ignore_dirs:
            builder.add_ignore_dir(ignore_dir)
        return self.search_count_base(builder)

    def search_count_maxdepth(self, glob_pattern, maxdepth):
        return self.search_count_base(MyGlobBuilder(glob_pattern).set_maxdepth(maxdepth))

    def test_search_1(self):
        base_path = str(self.test_dir).replace('\\', '/')
        
        # Basic testing
        self.assertEqual(self.search_count(f"{base_path}/info"), (1, 0))
        self.assertEqual(self.search_count(f"{base_path}/*"), (2, 3))
        self.assertEqual(self.search_count(f"{base_path}/*.*" ), (1, 0))
        self.assertEqual(self.search_count(f"{base_path}/fruits/*"), (4, 0))
        self.assertEqual(self.search_count(f"{base_path}/{{fruits,légumes}}/p*"), (3, 0))
        self.assertEqual(self.search_count(f"{base_path}/**/p*"), (3, 0))
        self.assertEqual(self.search_count(f"{base_path}/**/*.txt"), (13, 0))
        self.assertEqual(self.search_count(f"{base_path}/**/*.*.*" ), (1, 0))
        self.assertEqual(self.search_count(f"{base_path}/légumes/*"), (3, 0))
        self.assertEqual(self.search_count(f"{base_path}/*s/to[a-z]a{{r,s,t}}e.t[xX]t"), (2, 0))

        # Multibyte characters
        self.assertEqual(self.search_count(f"{base_path}/**/*爱*/*a*.txt"), (1, 0))
        self.assertEqual(self.search_count(f"{base_path}/**/*爱*/**/*a*.txt"), (3, 0))
        self.assertEqual(self.search_count(f"{base_path}/我爱你/**/*🐗*"), (1, 0))

        # Testing autorecurse
        self.assertEqual(self.search_count(f"{base_path}/*.txt"), (1, 0))
        self.assertEqual(self.search_count_autorecurse(f"{base_path}/*.txt"), (13, 0))
        self.assertEqual(self.search_count(f"{base_path}"), (0, 1))
        self.assertEqual(self.search_count_autorecurse(f"{base_path}"), (14, 4))
        self.assertEqual(self.search_count_autorecurse(f"{base_path}/"), (14, 4))

        # Testing ignore
        self.assertEqual(self.search_count_ignore(f"{base_path}/**/*.txt", ["Légumes"]), (10, 0))
        self.assertEqual(self.search_count_ignore(f"{base_path}/**/*.txt", ["Légumes", "我爱你"]), (5, 0))

        # Testing maxdepth
        self.assertEqual(self.search_count_maxdepth(f"{base_path}/**/*.txt", 1), (10, 0))
        self.assertEqual(self.search_count_maxdepth(f"{base_path}/**/*.txt", 2), (13, 0))

    def test_search_error_1(self):
        with self.assertRaises(MyGlobError):
            MyGlobBuilder("C:/**z//z").compile()

    def test_search_error_2(self):
        with self.assertRaises(MyGlobError):
            MyGlobBuilder("C:[Hello").compile()

if __name__ == '__main__':
    unittest.main()
