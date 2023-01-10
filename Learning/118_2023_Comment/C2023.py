# Add 2023 Net7 comment to Visual Studio Projects
#
# 2023-01-10    PV
#

from common_fs import *
import codecs

root = r'C:\Development\GitHub\Visual-Studio-Projects\Net7'
files = [f for f in get_all_files(root) if extension(f.lower()) in ['.cs', '.vb', '.cpp'] and 'designer' not in f.lower() and '.g.i.' not in f.lower()
         and 'assemblyinfo' not in f.lower() and 'assemblyattributes' not in f.lower()]


def ProcessFile(filefp: str, commenttoken: str, commentline: str):
    path, file = os.path.split(filefp)
    base, ext = os.path.splitext(file)

    lines: list[str]
    data = open(filefp, "rb").read()
    if data.startswith(codecs.BOM_UTF8):
        lines = codecs.decode(data, encoding='utf_8_sig', errors='strict').split('\r\n')
    else:
        # Either UTF-8 without BOM or ANSI
        # Since UTF-8 is strict on encoding, try it first, it it fails, then assume it's ANSI
        try:
            lines = codecs.decode(data, encoding='utf_8', errors='strict').split('\r\n')
        except:
            lines = codecs.decode(data, encoding='mbcs', errors='strict').split('\r\n')

    # If first line does not start with a comment, skip it (ex: App.xaml.cs)
    if not lines[0].startswith(commenttoken):
        return

    lnum = 1
    while lnum < len(lines) and lines[lnum].startswith(commenttoken):
        lnum += 1

    # If commentline is already present, don't insert it again
    if lines[lnum-1]==commentline:
        return

    with open(filefp, 'w', encoding='utf_8_sig') as fout:
        for i in range(lnum):
            fout.write(lines[i]+'\n')
        fout.write(commentline+'\n')
        for i in range(lnum, len(lines)):
            fout.write(lines[i]+'\n')

    print(filefp)

def ProcessCXFile(fn: str):
    ProcessFile(fn, '//', '// 2023-01-10\tPV\t\tNet7')

def ProcessVBFile(fn: str):
    ProcessFile(fn, "'", "' 2023-01-10\tPV\t\tNet7")

for file in files:
    match extension(file.lower()):
        case '.cs':
            #ProcessCXFile(file)
            pass
        case '.vb':
            #ProcessVBFile(file)
            pass
        case '.cpp':
            ProcessCXFile(file)
            pass
