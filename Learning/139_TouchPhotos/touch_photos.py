# touch_photos.py
# Ensure that pics last modified matches folder date
#
# Plexif: (since Pillow completely change image size/quality by default when saving, I just want to update exif data, not touch image part)
# https://stackoverflow.com/questions/33031663/how-to-change-image-captured-date-in-python
#
# 2024-09-05    PV

from common_fs import extension_part, file_part

import piexif
from PIL import Image
from PIL.ExifTags import TAGS
import os
from datetime import datetime, timedelta
import re

def get_date_taken(image_path):
    """
    Extracts the date taken from an image's EXIF data.
    """
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()        # type: ignore

        if exif_data:
            for tag_id, value in exif_data.items():
                tag_name = TAGS.get(tag_id, tag_id)
                if tag_name == 'DateTimeOriginal':
                    return datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
        else:
            return None  # No EXIF data found
    except (IOError, OSError):
        return None  # Error opening image

def update_date_taken(filename: str, new_date: datetime):
    exif_dict = piexif.load(filename)
    try:
        piexif.remove(filename)
        new_date_str = new_date.strftime("%Y:%m:%d %H:%M:%S")
        exif_dict['0th'][piexif.ImageIFD.DateTime] = new_date_str
        exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = new_date_str
        exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = new_date_str
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, filename)
        print(f"Updated date taken for {filename} to {new_date}")
    except:
        print("*** An error occurred")

# Use of Pillow change image size, divided by two for the first test file!!!
# I just want to update exif data, not update the image part...
# --> use piexif instead

# def update_date_taken(image_path: str, new_date: datetime):
#     """
#     Updates an image's date taken property in its EXIF data.
#     """
    
#     # try:
#     img = Image.open(image_path)
#     exif_data = img.getexif() or {}        # type: ignore

#     # Convert the new date to the required format
#     new_date_str = new_date.strftime('%Y:%m:%d %H:%M:%S')

#     exif_data[36867] = new_date_str  # 36867 is the tag ID for DateTimeOriginal
#     exif_data[36868] = new_date_str  # 36868 is the tag ID for DateTimeDigitized

#     img.save(image_path.replace(".jpg", "-upd.jpg"), exif=exif_data)
#     print(f"Updated date taken for {image_path} to {new_date}")

#     pass
#     breakpoint()
#     # except (IOError, OSError):
#     #     print(f"Error updating date taken for {image_path}")


"""
# Example usage
image_file = "C:\\PicturesODPerso\\2003 and before\\1999-02 Chicago\\Chicago 1999 - 04.jpg"

# Get the current date taken
current_date = get_date_taken(image_file)
if current_date:
    print(f"Current date taken: {current_date}")
else:
    print("Date taken not found or image format not supported.")

# Update the date taken (uncomment and modify as needed)
# new_date = datetime(2023, 12, 25, 10, 30, 0)  # Set your desired new date
# update_date_taken(image_file, new_date)
"""

def touch(source:str, dest:str):
  """
  Updates the last modified time of the 'dest' file using the last modified time of the 'source' file.

  Args:
      source: The path to the source file.
      dest: The path to the destination file.
  """

  source_mtime = os.path.getmtime(source)
  os.utime(dest, (source_mtime, source_mtime))


extract_YM_re = re.compile(r'^(\d{4})-(\d\d)(-(\d\d))? ')

#source = r'C:\PicturesODPerso\2011'
source = r'C:\PicturesPersoHR\2011'
doit = True

for root, subs, files in os.walk(source):
    if '\\A_Trier' in root:
        continue

    folder = file_part(root)
    if folder in ['2005-12 Pics famille 4x6', '2006-06 Jeff', '2006-08-25 Pics CR', '2006-09-10 Pics CR', '2019-11 Nantes', '2021-06-12 Gaufrier+RPi', '2023-03-15 Compteur gaz', '2024-01-04 Pics appartement pour PhG']:
        continue

    # print('root=', root)
    # print('folder=', folder)
    ma = extract_YM_re.match(folder)
    if ma:
        y = int(ma.group(1))
        m = int(ma.group(2))
        if ma.group(4):
            d = int(ma.group(4))
            # print("DateYMD=", y, m, d)
            d1 = datetime(y, m, d)
            dmin = d1 - timedelta(days=10)
            dmax = d1 + timedelta(days=14)
        else:
            # print("DateYM=", y, m)
            d1 = datetime(y, m, 1)
            dmin = d1 - timedelta(days=10)
            if m == 12:
                dmax = datetime(y + 1, 1, 1) + timedelta(days=10)
            else:
                dmax = datetime(y, m + 1, 1) + timedelta(days=14)

        lastdate = d1 + timedelta(hours=12)
        for file in sorted(files):
            filefp = os.path.join(root, file)
            if extension_part(filefp).lower() == ".jpg":
                #filefpLocal = filefp.replace(r'\\terazalt\photo\Pierre\PicturesODPerso', r'C:\PicturesODPerso')
                d = get_date_taken(filefp)
                if d:
                    if not (dmin <= d <= dmax):
                        lastdate += timedelta(seconds=1)
                        print("Not in range: ", d, ' ∉ [', dmin, ' .. ', dmax, '] ', filefp, ' -> ', lastdate, sep='')
                        if doit:
                            update_date_taken(filefp, lastdate)
                            #touch(filefp, filefpLocal)
                    else:
                        lastdate = d
                else:
                    lastdate += timedelta(seconds=1)
                    print("No date:", filefp, '->', lastdate)
                    if doit:
                        update_date_taken(filefp, lastdate)
                        #touch(filefp, filefpLocal)
    else:
        if not subs:
            pass
