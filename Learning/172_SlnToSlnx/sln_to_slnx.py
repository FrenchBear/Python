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

from common_fs import get_folders
import os


def convert_sln_to_slnx(target_directory):
    """
    Scans the directory and subfolders to replace a .sln file with a .slnx file
    only if strict file count conditions are met.
    """
    sln_files = []
    csproj_files = []
    slnx_files = []

    # 1. Walk the directory tree to count specific file types
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

    # 2. Check conditions
    # Must have exactly 1 .sln, 1 .csproj, and 0 .slnx
    if len(sln_files) != 1 or len(csproj_files) != 1 or len(slnx_files) != 0:
        print("Conditions not met for folder", target_directory)
        print(f"Found: {len(sln_files)} .sln files, {len(csproj_files)} .csproj files, {len(slnx_files)} .slnx files.")
        return

    # 3. Prepare paths and content
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

    # 4. Write new file and rename old one
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

# Example usage:
# convert_sln_to_slnx(r"C:\MyRepository\ProjectRoot")



#for folder in get_folders(r'C:\Development\GitVSTS\CSMisc\Net10', True):
for folder in get_folders(r'C:\Development\GitVSTS\CSMisc\Net10\CS90_MyGlob', True):
    print(folder)
    convert_sln_to_slnx(folder)
