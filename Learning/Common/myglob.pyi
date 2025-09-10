# myglob.pyi

import os
import re
from pathlib import Path
from collections import deque
from typing import Iterator, NamedTuple, Deque, Optional, Self, Tuple, cast

# -----------------------------------
# Globals

LIB_VERSION: str

# -----------------------------------
# Structures and Enums

class SegmentType:
    Constant: int
    Recurse: int
    Filter: int

class Segment:
    type: int
    value: str | re.Pattern | None
    def __init__(self, segment_type: int, value: str | re.Pattern | None = ...) -> None: ...
    def __repr__(self) -> str: ...

class MyGlobError(Exception): ...

class MyGlobMatch:
    path: Path
    is_dir: bool
    is_file: bool
    error: Optional[OSError]
    def __init__(self, path: Path, is_dir: bool = ..., is_file: bool = ..., error: Optional[OSError] = ...) -> None: ...
    def __repr__(self) -> str: ...

class SearchPendingDataFile(NamedTuple):
    path: Path
    def __init__(self, path: Path) -> None: ...

class SearchPendingDataDir(NamedTuple):
    path: Path
    def __init__(self, path: Path) -> None: ...

class SearchPendingDataDirToExplore(NamedTuple):
    path: Path
    depth: int
    recurse: bool
    recurse_depth: int
    def __init__(self, path: Path, depth: int, recurse: bool, recurse_depth: int) -> None: ...

class SearchPendingDataError(NamedTuple):
    err: OSError
    def __init__(self, err: OSError) -> None: ...

SearchPendingData = SearchPendingDataFile | SearchPendingDataDir | SearchPendingDataDirToExplore | SearchPendingDataError

class MyGlobSearch:
    root: Path
    segments: list[Segment]
    ignore_dirs: list[str]
    maxdepth: int
    def __init__(self, root: Path, segments: list[Segment], ignore_dirs: list[str], maxdepth: int) -> None: ...
    @staticmethod
    def version() -> str: ...
    @staticmethod
    def glob_syntax() -> str: ...
    def is_constant(self) -> bool: ...
    def explore(self) -> Iterator[MyGlobMatch]: ...

class MyGlobBuilder:
    glob_pattern: str
    ignore_dirs: list[str]
    maxdepth: int
    autorecurse: bool
    def __init__(self, glob_pattern: str) -> None: ...
    def add_ignore_dir(self, d: str) -> Self: ...
    def set_maxdepth(self, depth: int) -> Self: ...
    def set_autorecurse(self, active: bool) -> Self: ...
    @staticmethod
    def get_root(glob_pattern: str) -> Tuple[str, str]: ...
    @staticmethod
    def glob_to_segments(glob_pattern: str) -> list[Segment]: ...
    def compile(self) -> MyGlobSearch: ...
