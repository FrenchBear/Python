from typing import Iterable
from common import get_safe_name
import os
import shutil

source = r'W:\TempBD\archives'
DO_IT = True


def get_folgers_with_just_one_sub(source: str) -> Iterable[str]:
    for root, subs, files in os.walk(source, False):
        if len(files)==0 and len(subs)==1:
            yield root

def move_content_up(folderfp: str, singlesub: str):
    singlesubfp = os.path.join(folderfp, singlesub)
    _, subs, files = next(os.walk(singlesubfp))
    for sub in subs:
        if DO_IT:
            os.rename(os.path.join(singlesubfp, sub),  get_safe_name(os.path.join(folderfp, sub)))
    print('  subs ', end='')
    for file in files:
        if DO_IT:
            os.rename(os.path.join(singlesubfp, file), get_safe_name(os.path.join(folderfp, file)))
    print('files ', end='')
    if DO_IT:
        _, subs, files = next(os.walk(singlesubfp))
        if len(subs)>0 or len(files)>0:
            breakpoint()
        shutil.rmtree(singlesubfp)
    print('rmdir')


for folderfp in list(get_folgers_with_just_one_sub(source)):
    _, subs, files = next(os.walk(folderfp))
    if len(subs)==1 and len(files)==0:
        singlesub = subs[0]
        print(f'{folderfp:<100} {singlesub}')
        move_content_up(folderfp, singlesub)
