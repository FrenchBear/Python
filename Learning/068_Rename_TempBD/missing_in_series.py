import os
from collections import defaultdict
import re

from common_fs import get_files


source = r"W:\TempBD\final"
extra_sources = [
    r"W:\BD\Classique",
    r"W:\BD\Adulte",
    r"W:\BD\Ancien",
    r"W:\BD\Extra",
    r"W:\BD\Comics",
]


folders: list[str]
_1, folders, _2 = next(os.walk(source))
folders.sort()

dic_min_num: dict[str, int]
dic_max_num: dict[str, int]
dic_nums: dict[str, set]


def process_folder(folderfp: str):
    global dic_min_num, dic_max_num, dic_nums
    files = get_files(folderfp)
    for file in files:
        stem, _ = os.path.splitext(file)
        if stem.lower().startswith("thumbs"):
            # try:
            #     os.remove(os.path.join(folderfp, file))
            # except:
            pass
        else:
            if ma := re.fullmatch(
                r"(.*)? - ((\d{2,3})[A-Z]?|Pub|HS|HS \d+|BO)( - .*)?",
                stem,
                re.IGNORECASE,
            ):
                try:
                    serie = ma.group(1).lower()
                    n = int(ma.group(3))
                    if serie not in dic_nums:
                        dic_min_num[serie] = n
                        dic_max_num[serie] = n
                    else:
                        dic_min_num[serie] = min(dic_min_num[serie], n)
                        dic_max_num[serie] = max(dic_max_num[serie], n)
                    dic_nums[serie].add(n)
                except:
                    pass


with open(r"missing_in_series.txt", "w", encoding="utf8") as out:
    for folder in folders:
        # if folder == 'Agatha Christie':
        #     breakpoint()
        dic_min_num = {}
        dic_max_num = {}
        dic_nums = defaultdict(set)
        folderfp = os.path.join(source, folder)
        process_folder(folderfp)
        for extra_source in extra_sources:
            extra_folderfp = os.path.join(extra_source, folder)
            if os.path.exists(extra_folderfp):
                process_folder(extra_folderfp)
            else:
                extra_folderfp = os.path.join(extra_source, folder + " ꜰ")
                if os.path.exists(extra_folderfp):
                    process_folder(extra_folderfp)

        for serie in dic_nums.keys():
            min_num = dic_min_num[serie]
            max_num = dic_max_num[serie]
            nums = dic_nums[serie]
            if (
                min_num <= 2
                and max_num - min_num >= 3
                and max_num - min_num <= len(nums) < max_num - min_num + 1
            ):
                print(f"{folder:<40} {serie:<40}")
                out.write(f"{folder:<40} {serie:<40} ")
                for n in range(min_num, max_num + 1):
                    if n not in nums:
                        out.write(f"{n:>02} ")
                out.write(f"     {min_num:>02}..{max_num:>02}\n")
