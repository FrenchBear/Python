# Update build.bat
# For build.bat containing "dotnet build", adds %* at the end
#
# 2024-12-30    PV

from io import TextIOWrapper
from common_fs import get_all_files, file_part
import codecs
import os

searchfile = 'build.bat'
searchline = 'dotnet build'
replaceline = 'dotnet build %*'

#searchfile = 'run.bat'
#searchline = 'dotnet run --no-build -- %1 %2 %3 %4 %5 %6 %7 %8 %9'
#replaceline = '@run_dotnet.bat %*'

root = r'C:\Development\GitVSTS\DevForFun'
#root = r'C:\Development\GitVSTS\DevForFun\01_Labyrinthe\VB_Net9'
logfile = r'C:\Temp\build.log'

files = [f for f in get_all_files(root) if file_part(f).lower() == searchfile and '.git' not in f.lower()
         and ('net8' in f.lower() or 'net9' in f.lower())]
DoIt = True


def ProcessBatchFile(flog: TextIOWrapper, filefp: str):
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
            try:
                lines = codecs.decode(data, encoding='cp1252', errors='strict').split('\r\n')
            except:
                lines = codecs.decode(data, encoding='mbcs', errors='strict').split('\r\n')

    updated = False
    for ix in range(len(lines)):
        if lines[ix].rstrip() == searchline:
            updated = True
            lines[ix] = replaceline

    # Remove final empty lines
    while lines[-1].strip() == '':
        del lines[-1]
        updated = True

    if updated:
        print(filefp)
        flog.write(f"{filefp}\n")
        for ix, line in enumerate(lines):
            print(f'  {ix + 1}: {line}')
            flog.write(f'  {ix + 1}: {line}\n')

        if DoIt:
            # .bat are NOT UTF-8 files
            with open(filefp, 'w', encoding='cp1252') as fout:
                for ix, line in enumerate(lines):
                    fout.write(line)
                    if ix != len(lines) - 1:
                        fout.write('\n')


print('Output ->', logfile)
with open(logfile, 'w', encoding='utf_8_sig') as flog:
    for file in files:
        ProcessBatchFile(flog, file)
