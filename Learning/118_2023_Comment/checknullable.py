# Check for net8 .cs files containing #nullable enable
#
# 2023-11-20    PV

from common_fs import get_all_files, extension_part, file_readalltext

nf = 0
for filefp in (f.lower() for f in get_all_files(r'c:\Development')):
    if 'net8' in filefp and extension_part(filefp) == '.cs':
        nf = nf + 1

        src = file_readalltext(filefp).lower()
        if '\n#nullable enable' in src:
            print('#nullable enable:', filefp)

print(nf, 'net8 .cs files found')
