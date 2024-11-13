# remove_interaction_logic.py
# Remove C# sources useless comments
#   /// <summary>
#   /// Interaction logic for App.xaml
#   /// </summary>
#
# 2023-10-15    PV

from common_fs import get_all_files, extension_part
import codecs
import os
import re


#root = r'C:\Development\GitVSTS\WPF\Net7\Learning'
#root = r'C:\Development\GitVSTS\CSMisc\Net7'
root = r'C:\Development\GitHub\Visual-Studio-Projects\Net7'

files = [f for f in get_all_files(root) if extension_part(f.lower()) == '.cs' and 'designer' not in f.lower() and '.g.i.' not in f.lower()
         and 'assemblyinfo' not in f.lower() and 'assemblyattributes' not in f.lower()]

il = re.compile(r'/// <summary>\r?\n/// Interaction logic for .*\r?\n/// </summary>\r?\n')

def ProcessFile(filefp: str) -> bool:
    path, file = os.path.split(filefp)
    base, ext = os.path.splitext(file)

    source: str
    data = open(filefp, "rb").read().replace(b'\r\n', b'\n')
    if data.startswith(codecs.BOM_UTF8):
        source = codecs.decode(data, encoding='utf_8_sig', errors='strict')
    else:
        # Either UTF-8 without BOM or ANSI
        # Since UTF-8 is strict on encoding, try it first, it it fails, then assume it's ANSI
        try:
            source = codecs.decode(data, encoding='utf_8', errors='strict')
        except:
            source = codecs.decode(data, encoding='mbcs', errors='strict')

    updated = False
    ma: re.Match[str] | None
    while (ma := re.search(il, source)):
        updated = True
        begin, end = ma.span()
        source = source[:begin] + source[end:]

    if updated:
        print(filefp)
        with open(filefp, 'w', encoding='utf-8_sig') as fout:
            fout.write(source )
        return True

    return False


nf = 0
nm = 0
for filefp in files:
    nf += 1
    if ProcessFile(filefp):
        nm += 1

print(nf, 'files, ', nm, 'matches')
