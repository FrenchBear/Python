# checkNet10.py
# Check for missed files in update Net9 -> Net10
#
# 2025-01-02    PV
# 2025-11-12    PV      Net10 version
# 2026-02-02    PV      Check more files

import os

doit = False

# No more xx_Net9 folder unless a xx_Net10 exists
def check_xxNet9():
    root_folder = r'C:\Development\GitVSTS\DevForFun'
    for (dirpath, dirnames, filenames) in os.walk(root_folder):
        if '.git' not in dirpath:
            for prefix in ['CS', 'VB', 'FS']:
                if prefix+'_Net9' in dirnames and prefix+'_Net10' not in dirnames:
                    print(f'{dirpath}: {prefix}_Net9 exists, but not {prefix}_Net10')

def check_Net10projects(root_folder: str):
    for (dirpath, dirnames, filenames) in os.walk(root_folder):
        if '.git' not in dirpath and 'Net10' in dirpath:
            for file in filenames:
                filefp = os.path.join(dirpath, file)
                for ext in ['.csproj', '.fsproj', '.vbproj']:        #, 'makefile']:
                    if file.lower().endswith(ext):
                        with open(filefp) as f:
                            s = f.read()
                        updated = False
                        if 'net9' in s.lower():
                            print(f'net9 found in {filefp}')
                            s = s.replace('>net9.0<', '>net10.0<').replace('>net9.0-windows<', '>net10.0-windows<').replace('Net9 C#13', 'Net10 C#14').replace('Net8 C#12', 'Net9 C#13').replace('\\net9.0\\', '\\net10.0\\').replace('Net9 F#', 'Net10 F#')
                            updated = True
                        if '-2025' in s:
                            print('-2025 in', filefp)
                            s = s.replace('-2025', '-2026')
                            updated = True
                        elif '2025' in s:
                            print('2025 in', filefp)
                            s = s.replace('2025', '2025-2026')
                            updated = True

                        if updated:
                            print('To update:', filefp)
                            if doit:
                                with open(filefp, 'w') as f:
                                    f.write(s)

                        # if '2024' not in s.lower():
                        #     print(f'2024 not found in {filefp}')
                if file in ['build.bat', 'run.bat', 'run.sh', 'Makefile', 'launch.json', 'tasks.json']:
                    with open(filefp) as f:
                        s = f.read()
                    if 'net8' in s.lower():
                        print(f'net8 found in {filefp}')
                    if 'net9' in s.lower():
                        print(f'net9 found in {filefp}')


#check_xxNet9()

d4fp = [
r'C:\Development\GitVSTS\DevForFun\01_Labyrinthe\FS_Net10',
r'C:\Development\GitVSTS\DevForFun\02_Hilbert\FS_Net10',
r'C:\Development\GitVSTS\DevForFun\03_Radoteur\FS_Net10',
r'C:\Development\GitVSTS\DevForFun\04_VietnamesePuzzle\FS_Net10',
r'C:\Development\GitVSTS\DevForFun\05_Percolator\FS_Net10',
r'C:\Development\GitVSTS\DevForFun\06_Generics\FS_Net10',
r'C:\Development\GitVSTS\DevForFun\08_EightQueens\FS_Net10',
r'C:\Development\GitVSTS\DevForFun\10_Permutator\FS_Net10',
r'C:\Development\GitVSTS\DevForFun\11_Primes\FS_Net10',
r'C:\Development\GitVSTS\DevForFun\14_SieveIterator\FS_Net10',
r'C:\Development\GitVSTS\DevForFun\15_TopoSort\FS_Net10',
r'C:\Development\GitVSTS\DevForFun\16_Formatting\FS_Net10',
r'C:\Development\GitVSTS\DevForFun\17_StringCoding\FS_Net10',
r'C:\Development\GitVSTS\DevForFun\19_Dijkstra\FS_Net10',
r'C:\Development\GitVSTS\DevForFun\20_Lex\FS_Net10',
r'C:\Development\GitVSTS\DevForFun\21_FractionDevelopment\FS_Net10',
]
for p in d4fp:
    check_Net10projects(p)
