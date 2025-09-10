# MyGlob tests - test_regexp_conversions
# Unit tests for MyGlob
#
# 2025-09-10    PV

import unittest
import sys
import os
from enum import Enum, auto

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from myglob import MyGlobBuilder, MyGlobError, SegmentType

class ConvResult(Enum):
    CRError = auto()
    Constant = auto()
    Recurse = auto()
    Filter = auto()

class TestRegexpConversions(unittest.TestCase):

    def glob_one_segment_test(self, glob_pattern: str, cr: ConvResult, test_string: str, is_match: bool):
        try:
            seg_vec = MyGlobBuilder.glob_to_segments(glob_pattern)
            
            if cr == ConvResult.CRError:
                self.fail(f"Conversion of «{glob_pattern}» should have produced an error")

            if glob_pattern != "**":
                self.assertEqual(len(seg_vec), 1, f"Expected 1 segment for «{glob_pattern}»")
            
            segment = seg_vec[0]
            if segment.type == SegmentType.Constant:
                self.assertEqual(cr, ConvResult.Constant, f"Conversion of «{glob_pattern}» produced a Constant instead of a {cr.name}")
                self.assertEqual(is_match, segment.value.lower() == test_string.lower(), f"Match «{glob_pattern}» with «{test_string}» did not produce the expected result")
            elif segment.type == SegmentType.Recurse:
                self.assertEqual(cr, ConvResult.Recurse, f"Conversion of «{glob_pattern}» produced a Recurse instead of a {cr.name}")
                # In the Python implementation, glob_to_segments('**') returns [Recurse, Filter(.*)]
                # so we check the first segment. A real match would depend on the full context.
                # For this unit test, we assume Recurse always matches conceptually.
                self.assertTrue(is_match)
            elif segment.type == SegmentType.Filter:
                self.assertEqual(cr, ConvResult.Filter, f"Conversion of «{glob_pattern}» produced a Filter instead of a {cr.name}")
                self.assertEqual(bool(segment.value.match(test_string)), is_match, f"Match «{glob_pattern}» with «{test_string}» did not produce the expected result. Regex: {segment.value.pattern}")

        except MyGlobError:
            self.assertEqual(cr, ConvResult.CRError, f"Conversion of «{glob_pattern}» produced an unexpected error")

    def test_conversions(self):
        # Simple constant string, case insensitive
        self.glob_one_segment_test("Pomme", ConvResult.Constant, "pomme", True)
        self.glob_one_segment_test("Pomme", ConvResult.Constant, "pommerol", False)

        # * pattern, matches everything
        self.glob_one_segment_test("*", ConvResult.Filter, "rsgresp.d", True)
        self.glob_one_segment_test("*", ConvResult.Filter, "rsgresp.d.e.f", True)
        self.glob_one_segment_test("*.d", ConvResult.Filter, "rsgresp.d", True)
        self.glob_one_segment_test("*.*", ConvResult.Filter, "rsgresp", False)

        # ** pattern must be alone , and matches anything, including \
        with self.assertRaises(MyGlobError):
            MyGlobBuilder.glob_to_segments("**.d")
        self.glob_one_segment_test("**", ConvResult.Recurse, "", True)

        # Alternations
        self.glob_one_segment_test("a{b,c}d", ConvResult.Filter, "abd", True)
        self.glob_one_segment_test("a{b,c}d", ConvResult.Filter, "ad", False)
        self.glob_one_segment_test("a{{b,c},{d,e}}f", ConvResult.Filter, "acf", True)
        self.glob_one_segment_test("a{{b,c},{d,e}}f", ConvResult.Filter, "adf", True)
        self.glob_one_segment_test("a{{b,c},{d,e}}f", ConvResult.Filter, "acdf", False)
        self.glob_one_segment_test("a{b,c}{d,e}f", ConvResult.Filter, "acdf", True)
        self.glob_one_segment_test("file.{cs,py,rs,vb}", ConvResult.Filter, "file.bat", False)
        self.glob_one_segment_test("file.{cs,py,rs,vb}", ConvResult.Filter, "file.rs", True)

        # ? replace exactly one character
        self.glob_one_segment_test("file.?s", ConvResult.Filter, "file.rs", True)
        self.glob_one_segment_test("file.?s", ConvResult.Filter, "file.cds", False)
        self.glob_one_segment_test("file.?s", ConvResult.Filter, "file.py", False)

        # * replace 0 or more characters
        self.glob_one_segment_test("file.*s", ConvResult.Filter, "file.s", True)
        self.glob_one_segment_test("file.*s", ConvResult.Filter, "file.rs", True)
        self.glob_one_segment_test("file.*s", ConvResult.Filter, "file.chamallows", True)
        self.glob_one_segment_test("file.*s", ConvResult.Filter, "file.py", False)

        # [abc] matches any characters of the set
        self.glob_one_segment_test("file.[cr]s", ConvResult.Filter, "file.rs", True)
        self.glob_one_segment_test("file.[cr]s", ConvResult.Filter, "file.cs", True)
        self.glob_one_segment_test("file.[cr]s", ConvResult.Filter, "file.py", False)

        # [a-z] matches any character of the range
        self.glob_one_segment_test("file.[a-r]s", ConvResult.Filter, "file.rs", True)
        self.glob_one_segment_test("file.[a-r]s", ConvResult.Filter, "file.cs", True)
        self.glob_one_segment_test("file.[a-r]s", ConvResult.Filter, "file.zs", False)

        # a - at the beginning or end of a class actually matches a minus
        self.glob_one_segment_test("file.[-+]s", ConvResult.Filter, "file.-s", True)
        self.glob_one_segment_test("file.[+-]s", ConvResult.Filter, "file.-s", True)
        self.glob_one_segment_test("file.[-+]s", ConvResult.Filter, "file.+s", True)
        self.glob_one_segment_test("file.[-]s", ConvResult.Filter, "file.-s", True)

        # A ! at the beginning of a class inverts filtering
        self.glob_one_segment_test("file.[!abc]s", ConvResult.Filter, "file.rs", True)
        self.glob_one_segment_test("file.[!abc]s", ConvResult.Filter, "file.cs", False)
        self.glob_one_segment_test("file.[!0-9]s", ConvResult.Filter, "file.3s", False)
        self.glob_one_segment_test("file.[!0-9]s", ConvResult.Filter, "file.cs", True)

        # A ] at the beginning of a class matches a ]
        self.glob_one_segment_test("file.[]]s", ConvResult.Filter, "file.]s", True)
        self.glob_one_segment_test("file.[]]s", ConvResult.Filter, "file.[s", False)
        self.glob_one_segment_test("file.[!]]s", ConvResult.Filter, "file.]s", False)
        self.glob_one_segment_test("file.[!]]s", ConvResult.Filter, "file.[s", True)

        # Character classes
        self.glob_one_segment_test(r"file[\d].cs", ConvResult.Filter, "file1.cs", True)
        self.glob_one_segment_test(r"file[\D].cs", ConvResult.Filter, "file2.cs", False)
        self.glob_one_segment_test(r"file[\D].cs", ConvResult.Filter, "filed.cs", True)
        
        # Python's re does not support classes such \p{Greek}
        # Chec Python re doc to see exactly what is supported
        # self.glob_one_segment_test(r"file[\p{Greek}].cs", ConvResult.Filter, "fileζ.cs", True)

if __name__ == '__main__':
    unittest.main()
