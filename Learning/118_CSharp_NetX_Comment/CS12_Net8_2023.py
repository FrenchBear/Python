# Add 2023 Net8 comment to Visual Studio Projects
# Don't forget to change the date!!!
#
# 2023-01-10    PV
# 2023-11-18    PV      Also add empty comment line before header and dates block

from io import TextIOWrapper
from common_fs import get_all_files, extension_part
import codecs
import os
import re

DATE = '2023-11-18'
root = r'C:\Development\GitVSTS\WPF\Net8\Learning'
root = r'C:\Development\GitVSTS\WPF\Net8\FontApps'
root = r'C:\Development\GitVSTS\CSMisc\Net8'
root = r'C:\Development\GitVSTS\BookApps\Net8'
root = r'C:\Development\GitVSTS\UIApps\Net8'
root = r'c:\development\github\visual-studio-projects\net8'

files = [f for f in get_all_files(root) if extension_part(f.lower()) in ['.cs', '.vb', '.cpp'] and 'designer' not in f.lower() and '.g.i.' not in f.lower()
         and 'assemblyinfo' not in f.lower() and 'assemblyattributes' not in f.lower()]
DATE_YM_RE = re.compile(r'[ \t]*(199\d|20[012]\d)-(0[1-9]|10|11|12)[ \t]+.*')
DATE_YMD_RE = re.compile(r'[ \t]*(199\d|20[012]\d)-(0[1-9]|10|11|12)-(0[1-9]|[12]\d|30|31)[ \t]+.*')
DATE_DUP_RE = re.compile(r'[ \t]*""""""""""[ \t]+.*')
Verbose = False
DoIt = True


def isDatedComment(commenttoken: str, line: str) -> bool:
    l2 = line[len(commenttoken):]
    return bool(DATE_YMD_RE.match(l2)) or bool(DATE_YM_RE.match(l2)) or bool(DATE_DUP_RE.match(l2))

# print(isDatedComment('//', '// 2012-04-23   PV'))
# print(isDatedComment('//', '// 2018-04-30   PV      .Net Framework 4.6.2/Windows 10 Creators Update/dpi scaling per monitor awareness'))
# print(isDatedComment('//', '// Play with FormattedText and DrawingVisuals'))
# print(isDatedComment('//', '// 2021-09-09   PV      3.1.1 Make a BookApps projet, to fix bug in WidePath() when length==1'))

def ProcessFile(flog: TextIOWrapper, filefp: str, commenttoken: str, commentline: str):
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
        if Verbose:
            flog.write('\n' + filefp + '\n')
            flog.write('Does not start with a comment, skipped\n')
        return

    lnum = 0
    state = 0
    inserted = False
    while lnum < len(lines) and lines[lnum].startswith(commenttoken):
        l = str.rstrip(lines[lnum])
        match state:
            # SOF
            case 0:
                if l == commenttoken:
                    state = 2
                elif isDatedComment(commenttoken, l):
                    # If there is no header description, don't insert a separation comment
                    state = 3
                else:
                    state = 1

            # Description header
            case 1:
                if l == commenttoken:
                    state = 2
                elif isDatedComment(commenttoken, l):
                    # Found a date without separation comment, insert it
                    inserted = True
                    lines.insert(lnum, commenttoken)
                    state = 3
                # else stay in

            # We found a separation token
            case 2:
                if l == commenttoken:
                    flog.write('\n' + filefp + '\n')
                    flog.write(f'Err: Double comment token line {lnum + 1}\n')
                    return
                elif isDatedComment(commenttoken, l):
                    state = 3
                else:
                    # It's Ok to have an empty comment separaor in large headers before date block
                    state = 1

            # We found date block
            case 3:
                # Only date comment are accepted here
                if not isDatedComment(commenttoken, l):
                    flog.write('\n' + filefp + '\n')
                    flog.write(f'Err: Non-date comment line {lnum + 1}\n')
                    return

        lnum += 1

    # If we've not reached state 3, there is no date comment, ignore the file
    if state != 3:
        if Verbose:
            flog.write('\n' + filefp + '\n')
            flog.write('No date coment block, skipped\n')
        return

    # If commentline is already present, don't insert it again
    # if lines[lnum - 1] == commentline:
    if 'Net8' in lines[lnum - 1]:
        if Verbose:
            flog.write('\n' + filefp + '\n')
            flog.write('Already contains new date comment, skipped\n')
        return

    if DoIt:
        flog.write('\n' + filefp + '\n')
        if inserted and Verbose:
            flog.write('Insert empty separator comment\n')
        with open(filefp, 'w', encoding='utf_8_sig') as fout:
            for i in range(lnum):
                fout.write(lines[i] + '\n')
            fout.write(commentline + '\n')
            for i in range(lnum, len(lines)):
                fout.write(lines[i])
                if i != len(lines) - 1:
                    fout.write('\n')
        if Verbose:
            flog.write('Updated\n')


def ProcessCXFile(flog: TextIOWrapper, fn: str):
    ProcessFile(flog, fn, '//', '// ' + DATE + '\tPV\t\tNet8 C#12')


def ProcessVBFile(flog: TextIOWrapper, fn: str):
    ProcessFile(flog, fn, "'", "' " + DATE + "\tPV\t\tNet8")


with open(r'C:\Temp\C2023.log', 'w', encoding='utf_8_sig') as flog:
    for file in files:
        match extension_part(file.lower()):
            case '.cs':
                ProcessCXFile(flog, file)
                pass
            case '.vb':
                ProcessVBFile(flog, file)
                pass
            case '.cpp':
                ProcessCXFile(flog, file)
                pass
