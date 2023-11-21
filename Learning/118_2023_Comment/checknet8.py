# Check for errors in net8 .csproj files
#
# 2023-11-20    PV

from common_fs import get_all_files, extension_part, file_readalltext

nf = 0
for filefp in (f.lower() for f in get_all_files(r'c:\Development')):
    if 'net8' in filefp and extension_part(filefp) == '.csproj':
        nf = nf + 1

        src = file_readalltext(filefp).lower()
        if '>net8.0' not in src:
            print('Missing >net8.0:', filefp)
        if 'net7' in src:
            print('Found net7', filefp)
        if 'c#11' in src:
            print('Found C#11', filefp)
        if '<nullable>enable</nullable>' not in src:
            print('Missing <Nullable>enable</Nullable>', filefp)

print(nf, 'net8 csproj files found')
