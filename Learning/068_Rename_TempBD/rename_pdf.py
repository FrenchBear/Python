import os
import re
from common import get_safe_name
from common_fs import get_all_folders, get_files


source = r"W:\TempBD\archives\pdf"
# source = r'W:\TempBD\archives\hybrid.pdf'
DO_IT = True


NUM = re.compile(r"(\d+)")
NUM_DOT_TITLE = re.compile(r"(\d+)\. ?(.+)")
NUM_DASH_TITLE = re.compile(r"(\d+) - (.+)")
HSNUM_DOT_TITLE = re.compile(r"HS(\d+)\. (.+)", flags=re.IGNORECASE)
TOME_NUM = re.compile(r"^Tome (\d+)", flags=re.IGNORECASE)
TOME_NUM_DASH_TITLE = re.compile(r"^Tome (\d+) - (.+)", flags=re.IGNORECASE)


def rename(folderfp: str, oldname: str, newname: str):
    print(f"{oldname} -> {newname}")
    if DO_IT:
        os.rename(
            os.path.join(folderfp, oldname),
            get_safe_name(os.path.join(folderfp, newname)),
        )


def format_num(num: str) -> str:
    return f"{int(num):02}"


def rename_file(folderfp: str, serie: str, file: str):
    stem, ext = os.path.splitext(file)
    if ma := NUM.fullmatch(stem):
        newname = serie + " - " + format_num(ma.group(1)) + ext
        rename(folderfp, file, newname)
        return
    if ma := NUM_DOT_TITLE.fullmatch(stem):
        newname = serie + " - " + format_num(ma.group(1)) + " - " + ma.group(2) + ext
        rename(folderfp, file, newname)
        return
    if ma := NUM_DASH_TITLE.fullmatch(stem):
        if serie != "666" and serie != "6666":
            newname = (
                serie + " - " + format_num(ma.group(1)) + " - " + ma.group(2) + ext
            )
            rename(folderfp, file, newname)
            return
    if ma := HSNUM_DOT_TITLE.fullmatch(stem):
        newname = serie + " - HS " + format_num(ma.group(1)) + " - " + ma.group(2) + ext
        rename(folderfp, file, newname)
        return
    if ma := TOME_NUM.fullmatch(stem):
        newname = serie + " - " + format_num(ma.group(1)) + ext
        rename(folderfp, file, newname)
        return
    if ma := TOME_NUM_DASH_TITLE.fullmatch(stem):
        newname = serie + " - " + format_num(ma.group(1)) + " - " + ma.group(2) + ext
        rename(folderfp, file, newname)
        return
    if ma := re.fullmatch(
        re.escape(serie) + r" (\d+)\. (.+)", stem, flags=re.IGNORECASE
    ):
        newname = serie + " - " + format_num(ma.group(1)) + " - " + ma.group(2) + ext
        rename(folderfp, file, newname)
        return
    if ma := re.fullmatch(
        re.escape(serie) + r" (Vol(ume)? )?(\d+)", stem, flags=re.IGNORECASE
    ):
        newname = serie + " - " + format_num(ma.group(3)) + ext
        rename(folderfp, file, newname)
        return


for folderfp in get_all_folders(source):
    _, folder = os.path.split(folderfp)
    for file in get_files(folderfp):
        series_segments = folder.split(" - ")
        rename_file(folderfp, series_segments[0], file)
