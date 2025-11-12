# checkNet9.py
# Check for missed files in update Net8 -> Net9
#
# 2025-01-02    PV
# 2025-11-12    PV      Net10 version

import os

doit = True

# No more xx_Net8 folder unless a xx_Net9 exists
def check_xxNet8():
    root_folder = r'C:\Development\GitVSTS\DevForFun'
    for (dirpath, dirnames, filenames) in os.walk(root_folder):
        if '.git' not in dirpath:
            for prefix in ['CS', 'VB', 'FS']:
                if prefix+'_Net8' in dirnames and prefix+'_Net9' not in dirnames:
                    print(f'{dirpath}: {prefix}_Net8 exists, but not {prefix}_Net9')

def check_Net10projects(root_folder: str):
    for (dirpath, dirnames, filenames) in os.walk(root_folder):
        if '.git' not in dirpath and 'Net10' in dirpath:
            for file in filenames:
                for ext in [".csproj", ".fsproj", ".vbproj"]:        #, "makefile"]:
                    if file.lower().endswith(ext):
                        filefp = os.path.join(dirpath, file)
                        with open(filefp, "r") as f:
                            s = f.read()
                        updated = False
                        if "net9" in s.lower():
                            print(f"net9 found in {filefp}")
                            s = s.replace(">net9.0<", ">net10.0<").replace(">net9.0-windows<", ">net10.0-windows<").replace("Net9 C#13", "Net10 C#14").replace("Net8 C#12", "Net9 C#13").replace("\\net9.0\\", "\\net10.0\\")
                            updated = True
                        # if "-2024" in s:
                        #     s = s.replace('-2024', '-2025')
                        #     updated = True
                        # elif "2024" in s:
                        #     s = s.replace('2024', '2024-2025')
                        #     updated = True

                        if updated:
                            print(filefp)
                            if doit:
                                with open(filefp, "w") as f:
                                    f.write(s)

                        # if "2024" not in s.lower():
                        #     print(f"2024 not found in {filefp}")


#check_xxNet8()

#check_Net10projects(r'C:\Development\GitVSTS\BookApps\Net10')
#check_Net10projects(r'C:\Development\GitVSTS\UIApps\Net10')
#check_Net10projects(r'C:\Development\GitVSTS\CSMisc\Net10')
check_Net10projects(r'C:\Development\GitVSTS\WPF\Net10')
