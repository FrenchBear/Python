# Check for errors in net8 .csproj files
#
# 2023-11-20    PV

from common_fs import get_all_files, extension_part, file_readalltext

nf = 0
for filefp in (f.lower() for f in get_all_files(r'c:\Development')):
    if 'net8' in filefp and extension_part(filefp) == '.csproj':
        nf = nf + 1

        src_case = file_readalltext(filefp)
        src = src_case.lower()
        if '>net8.0' in src or '>net9.0' in src:
            print('Missing >net8.0:', filefp)
        # if 'net7' in src:
        #     print('Found net7', filefp)
        # if 'c#11' in src:
        #     print('Found C#11', filefp)
        # if '<nullable>enable</nullable>' not in src:
        #     print('Missing <Nullable>enable</Nullable>', filefp)
        # if '-2021' in src:
        #     src_case = src_case.replace('-2021', '-2023')
        #     with open(filefp, 'w', encoding='utf_8_sig') as fout:
        #         fout.write(src_case.replace('\r\n', '\n'))
        #     src = src_case.lower()

        if '2024' not in src:
            print('2024 missing:', filefp)

print(nf, 'net8/net9 csproj files found')
