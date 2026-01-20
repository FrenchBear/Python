# slnx.py
# Conversion from old .sln files into modern .slnx files
#
# 2026-01-11    PV

"""
I'd like Python function taking a path as parameter, designed to replace a .sln file (a Visual Studio solution file) with the new format .slnx
This transformation should occur only if the path and all its subfolders only contain one .sln file, one .csproj file and zero .slnx file. If these conditions are not met, a message should be printer and the function returns with no change.
If the conditions are met, a nex .slnx UTF-8 file should be created with following content between lines of dashes:
------------------------
<Solution>
  <Project Path="XXX.csproj" />
</Solution>
------------------------
where XXX.csproj is the name of the unique .csproj file found.
If this .slnx file is successfully written, then rename .sln file using .sln.bak suffix.
"""

from common_fs import get_all_folders
import os

doit = True


def convert_sln_to_slnx(target_directory):
    """
    Scans the directory and subfolders to replace a .sln file with a .slnx file
    only if strict file count conditions are met.
    """
    sln_files = []
    csproj_files = []
    slnx_files = []

    # Walk the directory tree to count specific file types
    for root, dirs, files in os.walk(target_directory):
        for file in files:
            # Case-insensitive check for extensions
            lower_file = file.lower()
            if lower_file.endswith('.sln'):
                sln_files.append(os.path.join(root, file))
            elif lower_file.endswith('.csproj'):
                csproj_files.append(os.path.join(root, file))
            elif lower_file.endswith('.slnx'):
                slnx_files.append(os.path.join(root, file))

    # Check conditions
    # Must have exactly 1 .sln, 1 .csproj, and 0 .slnx
    if len(sln_files) != 1 or len(csproj_files) != 1 or len(slnx_files) != 0:
        print("Conditions not met for folder", target_directory)
        print(f"Found: {len(sln_files)} .sln files, {len(csproj_files)} .csproj files, {len(slnx_files)} .slnx files.")
        return

    # Prepare paths and content
    sln_path = sln_files[0]
    csproj_path = csproj_files[0]
    
    # Get the name of the csproj file (XXX.csproj)
    csproj_name = os.path.basename(csproj_path)
    
    # Determine the path for the new .slnx file 
    # (Same directory and base name as the .sln file)
    sln_dir = os.path.dirname(sln_path)
    sln_filename = os.path.basename(sln_path)
    slnx_filename = os.path.splitext(sln_filename)[0] + ".slnx"
    slnx_full_path = os.path.join(sln_dir, slnx_filename)

    slnx_content = f"""<Solution>
  <Project Path="{csproj_name}" />
</Solution>"""

    # Write new file and rename old one
    if doit:
        try:
            # Write the .slnx file in UTF-8
            with open(slnx_full_path, 'w', encoding='utf-8') as f:
                f.write(slnx_content)
            
            # Rename the original .sln file
            bak_path = sln_path + ".bak"
            if os.path.exists(bak_path):
                os.remove(bak_path)
            os.rename(sln_path, bak_path)
            
            print(f"Success: Created '{slnx_filename}' and renamed original to '{os.path.basename(bak_path)}'.")

        except OSError as e:
            print(f"Error during file operation: {e}")


for root in [
    r"C:\Development\GitVSTS\DevForFun\01_Labyrinthe\CS_Net10",
    r"C:\Development\GitVSTS\DevForFun\01_Labyrinthe\CS_WPF_Net10",
    r"C:\Development\GitVSTS\DevForFun\02_Hilbert\CS_Net10",
    r"C:\Development\GitVSTS\DevForFun\03_Radoteur\CS_Net10",
    r"C:\Development\GitVSTS\DevForFun\04_VietnamesePuzzle\CS_Net10",
    r"C:\Development\GitVSTS\DevForFun\05_Percolator\CS_Net10",
    r"C:\Development\GitVSTS\DevForFun\06_Generics\CS_Net10",
    r"C:\Development\GitVSTS\DevForFun\08_EightQueens\CS_Net10",
    r"C:\Development\GitVSTS\DevForFun\10_Permutator\CS_Net10",
    r"C:\Development\GitVSTS\DevForFun\11_Primes\CS_Net10",
    r"C:\Development\GitVSTS\DevForFun\12_ArithDoubler\CS_Net10",
    r"C:\Development\GitVSTS\DevForFun\13_SegmentedSieve\CS_Net10",
    r"C:\Development\GitVSTS\DevForFun\14_SieveIterator\CS_Net10",
    r"C:\Development\GitVSTS\DevForFun\15_TopoSort\CS_Net10",
    r"C:\Development\GitVSTS\DevForFun\16_Formatting\CS_Net10",
    r"C:\Development\GitVSTS\DevForFun\17_StringCoding\CS_Net10",
    r"C:\Development\GitVSTS\DevForFun\18_ConfigFiles\CS_Net10",
    r"C:\Development\GitVSTS\DevForFun\19_Dijkstra\CS_Net10",
    r"C:\Development\GitVSTS\DevForFun\20_Lex\CS_Net10",
    r"C:\Development\GitVSTS\DevForFun\21_FractionDevelopment\CS_Net10",
    r"C:\Development\GitVSTS\DevForFun\22_Pentamino\CS_Net10",
    r"C:\Development\GitVSTS\DevForFun\23_Regex\CS_Net10",
    r"C:\Development\GitVSTS\DevForFun\24_Parallel\CS_Net10",
    r"C:\Development\GitVSTS\DevForFun\25_SQL\CS_Net10",
    r"C:\Development\GitVSTS\DevForFun\26_RotorRouter\CS_Net10",
    ]:
    print(root)
    convert_sln_to_slnx(root)
    for folder in get_all_folders(root):
        print(folder)
        convert_sln_to_slnx(folder)
