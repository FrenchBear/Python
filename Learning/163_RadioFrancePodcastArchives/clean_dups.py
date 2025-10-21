# Remove duplicates

# I need a python program to clean duplicate files in a Windows folder.
#
# In folder, I have .mp3 and .m4a files in folder "C:\Users\Pierr\Downloads\Podcasts\Lisa Delmoitiez\temp"
#
# Some files having same basename are duplicates, differing only by extension, such as "2025-10-17 - Je suis contre les
# frigos.m4a" and "2025-10-17 - Je suis contre les frigos.mp3"
#
# If I have both .m4a and .mp3 versions, I want to keep .m4a version and delete .mp3 version.
#
# If I have only .mp3 version, I want to keep it.
#
# Duplicates should be deleted to Windows recycle bin

import os
from pathlib import Path
from send2trash import send2trash

# --- Configuration ---
# Set the path to the folder you want to clean
TARGET_FOLDER = r"C:\Users\Pierr\Downloads\Podcasts\Lisa Delmoitiez\temp"
# ---------------------

def clean_duplicate_audio(folder_path_str):
    """
    Scans a folder for .mp3 and .m4a files.
    If a file exists with both extensions (e.g., file.mp3 and file.m4a),
    it moves the .mp3 version to the recycle bin.
    """
    
    target_dir = Path(folder_path_str)

    # 1. Check if the folder exists
    if not target_dir.is_dir():
        print(f"Error: Folder not found at: {folder_path_str}")
        print("Please check the 'TARGET_FOLDER' variable in the script.")
        return

    print(f"Scanning folder: {target_dir}\n")

    # 2. Create sets to store the basenames (filenames without extension)
    m4a_basenames = set()
    mp3_basenames = set()

    # 3. Scan the directory and populate the sets
    for file in target_dir.iterdir():
        # Check if it's a file (and not a directory)
        if file.is_file():
            if file.suffix == ".m4a":
                m4a_basenames.add(file.stem)  # .stem is the filename without extension
            elif file.suffix == ".mp3":
                mp3_basenames.add(file.stem)

    # 4. Find the basenames that are in *both* sets
    # These are the files where we have both .m4a and .mp3 versions
    duplicates_to_delete = m4a_basenames.intersection(mp3_basenames)

    if not duplicates_to_delete:
        print("No duplicate .mp3 files found to clean. All files are unique.")
        print("Done.")
        return

    print(f"Found {len(duplicates_to_delete)} .mp3 file(s) that are duplicates of .m4a files.")

    # 5. Iterate through the duplicates and delete the .mp3 version
    deleted_count = 0
    for basename in duplicates_to_delete:
        # Re-create the full path to the .mp3 file to be deleted
        mp3_file_path = target_dir / (basename + ".mp3")
        
        # Double-check it exists before trying to delete
        if mp3_file_path.exists():
            try:
                # Use send2trash to move to recycle bin
                # send2trash requires the path as a string
                send2trash(str(mp3_file_path))
                print(f"  [Recycled] {mp3_file_path.name}")
                deleted_count += 1
            except Exception as e:
                print(f"  [Error] Could not delete {mp3_file_path.name}: {e}")
        else:
            # This should not happen based on our logic, but it's a good safety check
            print(f"  [Warning] Wanted to delete {mp3_file_path.name}, but it was not found.")

    print(f"\nDone. Moved {deleted_count} .mp3 file(s) to the recycle bin.")

# --- Main execution ---
if __name__ == "__main__":
    clean_duplicate_audio(TARGET_FOLDER)
    