# 02_ResizePics.py
# Normalize pics size
#
# 2025-09-11    PV

from skimage.io import imread
import cv2
from PIL import Image, ImageEnhance
import os
from common_fs import get_files

source = r"D:\Pierre\OneDrive\PicturesODMisc\PLS573\Originaux"
target = r"D:\Pierre\OneDrive\PicturesODMisc\PLS573\Resized 2"

target_width = int(4900/2.5)
target_height = int(6700/2.5)

def process_file(filefp: str, dest: str, skip_enhance:bool=False):
    try:
        print(filefp)
        img = imread(filefp)
        img = cv2.resize(img, (target_width, target_height), interpolation=cv2.INTER_LANCZOS4)
        img = Image.fromarray(img)
        if not skip_enhance:
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.6)
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(2.5)
        img.save(dest, dpi=(600, 600))
    except Exception as e:
        return f"Error processing {filefp}: {e}"

def crop_and_resize(deskewed_img, target_width, target_height):
    return cv2.resize(deskewed_img, (target_width, target_height), interpolation=cv2.INTER_LANCZOS4)

def process_dir():
    os.makedirs(target, exist_ok=True)
    for filefp in get_files(source, True):
        dest = filefp.replace(source, target)
        process_file(filefp, dest)

if __name__ == '__main__':
    process_dir()
