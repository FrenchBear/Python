# checkNet9.py
# Check for missed files in update Net8 -> Net9
#
# 2025-01-02    PV

import os

# No more xx_Net8 folder unless a xx_Net9 exists
def check_xxNet8():
    root_folder = r'C:\Development\GitVSTS\DevForFun'
    for (dirpath, dirnames, filenames) in os.walk(root_folder):
        if '.git' not in dirpath:
            for prefix in ['CS', 'VB', 'FS']:
                if prefix+'_Net8' in dirnames and prefix+'_Net9' not in dirnames:
                    print(f'{dirpath}: {prefix}_Net8 exists, but not {prefix}_Net9')

def check_Net9projects(root_folder: str):
    for (dirpath, dirnames, filenames) in os.walk(root_folder):
        if '.git' not in dirpath and 'Net9' in dirpath:
            for file in filenames:
                for ext in [".csproj", ".fsproj", ".vbproj"]:        #, "makefile"]:
                    if file.lower().endswith(ext):
                        filefp = os.path.join(dirpath, file)
                        with open(filefp) as f:
                            s = f.read()
                        updated = False
                        # if "net8" in s.lower():
                        #     print(f"net8 found in {filefp}")
                        #     s = s.replace(">net8.0<", ">net9.0<").replace(">net8.0-windows<", ">net9.0-windows<").replace("C#12 Net8", "Net9 C#13").replace("Net8 C#12", "Net9 C#13").replace("\\net8.0\\", "\\net9.0\\")
                        #     updated = True
                        if "-2024" in s:
                            s = s.replace('-2024', '-2025')
                            updated = True
                        elif "2024" in s:
                            s = s.replace('2024', '2024-2025')
                            updated = True

                        if updated:
                            print(filefp)
                            with open(filefp, "w") as f:
                                f.write(s)
                            l = len(s)

                        # if "2024" not in s.lower():
                        #     print(f"2024 not found in {filefp}")


#check_xxNet8()
#check_Net9projects(r'C:\Development\GitVSTS\DevForFun')
check_Net9projects(r'C:\Development\GitVSTS')
#check_Net9projects(r'C:\Development\GitHub')

