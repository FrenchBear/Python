# my_glob library
# ORIGINAL FILE in C:\Development\GitHub\Python\Libraries
# After update, copy this file to C:\Development\GitHub\Python\Learning\Common
#
# Python translation of an efficient glob implementation in Rust
#
# 2025-09-10   PV      First Python version, partially translated by Gemini, debugged and refactored by me
# 2025-09-13   PV      1.0.1 Check for unclosed brackets in glob expressions such as "C:\[a-z"

import os
import re
from pathlib import Path
from collections import deque
from typing import Iterator, NamedTuple, Deque, Optional, Self, Tuple, cast

# -----------------------------------
# Globals

LIB_VERSION = "1.0.1"

# -----------------------------------
# Structures and Enums

class SegmentType:
    Constant = 1
    Recurse = 2
    Filter = 3

class Segment:
    def __init__(self, segment_type: int, value: str | re.Pattern | None = None) -> None:
        self.type = segment_type
        self.value = value

    def __repr__(self):
        if self.type == SegmentType.Constant:
            return f"Constant({self.value})"
        if self.type == SegmentType.Recurse:
            return "Recurse"
        if self.type == SegmentType.Filter:
            return f"Filter({self.value})"
        return "Segment"

class MyGlobError(Exception):
    pass

class MyGlobMatch:
    def __init__(self, path: Path, is_dir=False, is_file=False, error: Optional[OSError] = None):
        self.path = path
        self.is_dir = is_dir
        self.is_file = is_file
        self.error = error

    def __repr__(self):
        if self.error:
            return f"Error({self.error})"
        kind = "Dir" if self.is_dir else "File"
        return f"{kind}({self.path})"

class SearchPendingDataFile(NamedTuple):
    path: Path

class SearchPendingDataDir(NamedTuple):
    path: Path

class SearchPendingDataDirToExplore(NamedTuple):
    path: Path
    depth: int
    recurse: bool
    recurse_depth: int

class SearchPendingDataError(NamedTuple):
    err: OSError


SearchPendingData = SearchPendingDataFile | SearchPendingDataDir | SearchPendingDataDirToExplore | SearchPendingDataError

class MyGlobSearch:
    def __init__(self, root: Path, segments: list[Segment], ignore_dirs: list[str], maxdepth: int) -> None:
        self.root = root
        self.segments = segments
        self.ignore_dirs = ignore_dirs
        self.maxdepth = maxdepth

    @staticmethod
    def version() -> str:
        return LIB_VERSION

    @staticmethod
    def glob_syntax() -> str:
        return """⌊Glob pattern rules⌋:
- ¬⟦?⟧ matches any single character.
- ¬⟦*⟧ matches any (possibly empty) sequence of characters.
- ¬⟦**⟧ matches the current directory and arbitrary subdirectories. To match files in arbitrary subdirectories, use ⟦**/*⟧. This sequence must form a single path component, so both ⟦**a⟧ and ⟦b**⟧ are invalid and will result in an error.
- ¬⟦[...]⟧ matches any character inside the brackets. Character sequences can also specify ranges of characters (Unicode order), so ⟦[0-9]⟧ specifies any character between 0 and 9 inclusive. Special cases: ⟦[[]⟧ represents an opening bracket, ⟦[]]⟧ represents a closing bracket. 
- ¬⟦[!...]⟧ is the negation of ⟦[...]⟧, it matches any characters not in the brackets.
- ¬The metacharacters ⟦?⟧, ⟦*⟧, ⟦[⟧, ⟦]⟧ can be matched by escaping them between brackets such as ⟦[\\?]⟧ or ⟦[\\[]⟧. When a ⟦]⟧ occurs immediately following ⟦[⟧ or ⟦[!⟧ then it is interpreted as being part of, rather than ending the character set, so ⟦]⟧ and NOT ⟦]⟧ can be matched by ⟦[]]⟧ and ⟦[!]]⟧ respectively. The ⟦-⟧ character can be specified inside a character sequence pattern by placing it at the start or the end, e.g. ⟦[abc-]⟧.
- ¬⟦{choice1,choice2...}⟧  match any of the comma-separated choices between braces. Can be nested, and include ⟦?⟧, ⟦*⟧ and character classes.
- ¬Character classes ⟦[ ]⟧ accept regex syntax such as ⟦[\\d]⟧ to match a single digit, see https://docs.python.org/3/library/re.html for supported syntax.

⌊Autorecurse glob pattern transformation⌋:
- ¬⟪Constant pattern⟫ (no filter, no ⟦**⟧) pointing to a directory: ⟦/**/*⟧ is appended at the end to search all files of all subdirectories.
- ¬⟪Patterns without ⟦**⟧ and ending with a filter⟫: ⟦/**⟧ is inserted before the final filter to find all matching files of all subdirectories.
"""

    def is_constant(self) -> bool:
        return not self.segments

    def explore(self) -> Iterator[MyGlobMatch]:
        # Internal enum for queue items
        class SearchPendingDataType:
            File, Dir, DirToExplore, Error = range(4)

        if not self.segments:
            p = Path(self.root)
            if p.is_file():
                yield MyGlobMatch(p, is_file=True)
            elif p.is_dir():
                yield MyGlobMatch(p, is_dir=True)
            return

        queue: Deque[SearchPendingData] = deque([SearchPendingDataDirToExplore(self.root, 0, False, 0)])

        while queue:
            item = queue.popleft()

            match item:
                case SearchPendingDataError(err):
                    yield MyGlobMatch(Path(), error=err)

                case SearchPendingDataFile(path):
                    yield MyGlobMatch(path, is_file=True)

                case SearchPendingDataDir(path):
                    yield MyGlobMatch(path, is_dir=True)

                case SearchPendingDataDirToExplore(root, depth, recurse, recurse_depth):
                    segment = self.segments[depth]

                    if segment.type == SegmentType.Constant:
                        pb = root / cast(Path, segment.value)
                        is_final_segment = depth == len(self.segments) - 1
                        if is_final_segment:
                            if pb.is_file():
                                queue.append(SearchPendingDataFile(pb))
                            elif pb.is_dir():
                                queue.append(SearchPendingDataDir(pb))
                        elif pb.is_dir():
                            queue.append(SearchPendingDataDirToExplore(pb, depth + 1, False, 0))

                        if recurse and (self.maxdepth == 0 or recurse_depth < self.maxdepth):
                            try:
                                for entry in os.scandir(root):
                                    if entry.is_dir(follow_symlinks=False):
                                        entry_path = Path(entry.path)
                                        fnlc = entry.name.lower()
                                        if not any(ie == fnlc for ie in self.ignore_dirs):
                                            queue.append(SearchPendingDataDirToExplore(entry_path, depth, True, recurse_depth + 1))
                            except OSError as e:
                                queue.append(SearchPendingDataError(e))

                    elif segment.type == SegmentType.Recurse:
                        queue.append(SearchPendingDataDirToExplore(root, depth + 1, True, 0))

                    elif segment.type == SegmentType.Filter:
                        re_filter = cast(re.Pattern, segment.value)
                        dirs_to_recurse = []
                        is_final_segment = depth == len(self.segments) - 1

                        try:
                            for entry in os.scandir(root):
                                entry_path = Path(entry.path)

                                if entry.is_file(follow_symlinks=False):
                                    if is_final_segment and re_filter.match(entry.name):
                                        queue.append(SearchPendingDataFile(entry_path))
                                elif entry.is_dir(follow_symlinks=False):
                                    flnc = entry.name.lower()
                                    if not any(ie == flnc for ie in self.ignore_dirs):
                                        if re_filter.match(entry.name):
                                            if self.maxdepth == 0 or recurse_depth < self.maxdepth:
                                                if is_final_segment:
                                                    queue.append(SearchPendingDataDir(entry_path))
                                                else:
                                                    queue.append(SearchPendingDataDirToExplore(entry_path, depth + 1, False, 0))
                                        dirs_to_recurse.append(entry_path)
                        except OSError as e:
                            queue.append(SearchPendingDataError(e))

                        if recurse and (self.maxdepth == 0 or recurse_depth < self.maxdepth):
                            for d in dirs_to_recurse:
                                queue.append(SearchPendingDataDirToExplore(d, depth, True, recurse_depth + 1))


class MyGlobBuilder:
    def __init__(self, glob_pattern: str) -> None:
        self.glob_pattern = glob_pattern
        self.ignore_dirs = [
            "$recycle.bin",
            "system volume information",
            ".git",
        ]
        self.maxdepth = 0
        self.autorecurse = False

    def add_ignore_dir(self, d: str) -> Self:
        self.ignore_dirs.append(d.lower())
        return self

    def set_maxdepth(self, depth: int) -> Self:
        if depth > 0:
            self.maxdepth = depth
        return self

    def set_autorecurse(self, active: bool) -> Self:
        self.autorecurse = active
        return self

    @staticmethod
    def get_root(glob_pattern: str) -> Tuple[str, str]:
        glob = glob_pattern
        if not glob:
            glob = "*"

        cut = 0
        # Find last separator before any glob char
        last_sep = -1
        for i, char in enumerate(glob):
            if char in "*?[{":
                cut = last_sep + 1 if last_sep != -1 else 0
                break
            if char in "/\\":
                last_sep = i
        else:  # no glob chars found
            cut = len(glob)

        root = glob[:cut]
        if not root:
            root = "."

        rem = glob[cut:]
        return root, rem

    @staticmethod
    def glob_to_segments(glob_pattern: str) -> list[Segment]:
        if not glob_pattern:
            return []

        # glob_pattern ends with / so no duplicate code to process last segment
        if not (glob_pattern.endswith('/') or glob_pattern.endswith('\\')):
            glob_pattern += '/'

        segments = []
        regex_buffer = ""
        constant_buffer = ""
        brace_depth = 0
        in_brackets = False

        it = iter(glob_pattern)
        for c in it:
            if c == '/' or c == '\\':
                if brace_depth > 0:
                    raise MyGlobError("Invalid / between { }")

                if constant_buffer == "**":
                    segments.append(Segment(SegmentType.Recurse))
                elif "**" in constant_buffer:
                    raise MyGlobError("Glob pattern ** must be alone between /")
                elif any(char in "*?[{" for char in constant_buffer):
                    if brace_depth > 0:
                        raise MyGlobError("Unclosed {")
                    repat = f"^{regex_buffer}$"
                    try:
                        segments.append(Segment(SegmentType.Filter, re.compile(repat, re.IGNORECASE)))
                    except re.error as e:
                        raise MyGlobError(f"Regex error for pattern «{repat}»: {e}")
                elif constant_buffer:
                    segments.append(Segment(SegmentType.Constant, constant_buffer))

                regex_buffer = ""
                constant_buffer = ""
                continue

            constant_buffer += c
            if c == '*':
                regex_buffer += ".*"
            elif c == '?':
                regex_buffer += "."
            elif c == '{':
                brace_depth += 1
                regex_buffer += '('
            elif c == ',' and brace_depth > 0:
                regex_buffer += '|'
            elif c == '}':
                brace_depth -= 1
                if brace_depth < 0:
                    raise MyGlobError("Extra closing }")
                regex_buffer += ')'
            elif c == '[':
                regex_buffer += '['
                in_brackets = True

                # Special case: ! at the beginning is negation
                # Peek at next char without consuming
                try:
                    next_c = glob_pattern[len(constant_buffer)]
                    if next_c == '!':
                        next(it)
                        constant_buffer += '!'
                        regex_buffer += '^'
                except IndexError:
                    pass

                while (inner_c := next(it, None)) is not None:
                    match inner_c:
                        case ']':
                            regex_buffer += inner_c
                            in_brackets = False
                            break

                        case '\\':
                            if next_c := next(it):
                                regex_buffer += '\\'
                                regex_buffer += next_c
                            else:
                                regex_buffer += '\\'  # Handle trailing backslash

                        case _:
                            regex_buffer += inner_c

            elif c in ".+()|^$":  # Characters with special meaning in regex
                regex_buffer += '\\' + c
            else:
                regex_buffer += c

        if in_brackets:
            raise MyGlobError("Unclosed [")

        if regex_buffer:
            raise MyGlobError("Invalid glob pattern")

        # If last segment is a **, append a Filter * to find everything
        if segments and segments[-1].type == SegmentType.Recurse:
            segments.append(Segment(SegmentType.Filter, re.compile("^.*$", re.IGNORECASE)))

        return segments

    def compile(self) -> MyGlobSearch:
        root, rem = MyGlobBuilder.get_root(self.glob_pattern)
        segments = MyGlobBuilder.glob_to_segments(rem)

        if self.autorecurse:
            if not segments:
                rootp = Path(root)
                if rootp.is_dir():
                    segments.append(Segment(SegmentType.Recurse))
                    segments.append(Segment(SegmentType.Filter, re.compile("^.*$", re.IGNORECASE)))
            else:
                is_recursive = any(s.type == SegmentType.Recurse for s in segments)
                if not is_recursive and segments[-1].type == SegmentType.Filter:
                    segments.insert(len(segments) - 1, Segment(SegmentType.Recurse))

        return MyGlobSearch(Path(root), segments, self.ignore_dirs, self.maxdepth)
