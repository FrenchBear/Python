# MyGlob tests - test_glob_expression
# Unit tests for MyGlob
#
# 2025-09-10    PV

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from myglob import MyGlobBuilder, SegmentType

class TestGlobExpression(unittest.TestCase):

    def test_glob_ending_with_recurse(self):
        # Special case, when a glob pattern ends with **, then * is automatically added
        res = MyGlobBuilder.glob_to_segments("**")
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].type, SegmentType.Recurse)
        self.assertEqual(res[1].type, SegmentType.Filter)
        self.assertEqual(res[1].value.pattern, "^.*$")

    def test_relative_glob(self):
        res = MyGlobBuilder.glob_to_segments("*/target")
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].type, SegmentType.Filter)
        self.assertEqual(res[1].type, SegmentType.Constant)
        self.assertEqual(res[1].value, "target")

    def test_get_root(self):
        self.tgr("", ".", "*")
        self.tgr("*", ".", "*")
        self.tgr("C:", "C:", "")
        self.tgr("C:\\", "C:\\", "")
        self.tgr("file.ext", "file.ext", "")
        self.tgr("C:file.ext", "C:file.ext", "")
        self.tgr("C:\\file.ext", "C:\\file.ext", "")
        self.tgr("path\\file.ext", "path\\file.ext", "")
        self.tgr("path\\*.jpg", "path\\", "*.jpg")
        self.tgr("path\\**\\*.jpg", "path\\", "**\\*.jpg")
        self.tgr("C:path\\file.ext", "C:path\\file.ext", "")
        self.tgr("C:\\path\\file.ext", "C:\\path\\file.ext", "")
        self.tgr("\\\\server\\share", "\\\\server\\share", "")
        self.tgr("\\\\server\\share\\", "\\\\server\\share\\", "")
        self.tgr("\\\\server\\share\\file.txt", "\\\\server\\share\\file.txt", "")
        self.tgr("\\\\server\\share\\path\\file.txt", "\\\\server\\share\\path\\file.txt", "")
        self.tgr("\\\\server\\share\\*.jpg", "\\\\server\\share\\", "*.jpg")
        self.tgr("\\\\server\\share\\path\\*.jpg", "\\\\server\\share\\path\\", "*.jpg")
        self.tgr("\\\\server\\share\\**\\*.jpg", "\\\\server\\share\\", "**\\*.jpg")

    def tgr(self, pat, root, rem):
        r, s = MyGlobBuilder.get_root(pat)
        self.assertEqual(r, root)
        self.assertEqual(s, rem)

if __name__ == '__main__':
    unittest.main()
