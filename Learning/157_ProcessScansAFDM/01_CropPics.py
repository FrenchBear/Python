# 01_CropPics.py
#
# 2025-09-19    PV      Version "Aux frontières des mathématiques"

import numpy as np
from typing import cast, Any
from numpy.typing import NDArray
import cv2
from PIL import Image
import os
from common_fs import get_files

source = r"C:\PicturesODMisc\Aux frontières des mathématiques\Scans"
target = r"C:\PicturesODMisc\Aux frontières des mathématiques\Cropped,Deskewed"

target_width = int(4900/2)
target_height = int(6700/2)

odd_cropTop = 75
odd_cropBottom = 400
odd_cropLeft = 75
odd_cropRight = 250

even_cropTop = 300
even_cropBottom = 175
even_cropLeft = 250
even_cropRight = 75

def find_skew_angle(gray, min_angle: float = -1.0, max_angle: float = 1.0, step: float = 0.02) -> float:
    """
    Finds the skew angle of a text image using the projection profile method.

    Args:
        image_path (str): The path to the input image file.
        min_angle (float): The minimum angle to check (in degrees).
        max_angle (float): The maximum angle to check (in degrees).
        step (float): The step size for checking angles (in degrees).

    Returns:
        float: The estimated skew angle in degrees. A positive value means
               the image is rotated clockwise.
    """
    # # 1. Image Pre-processing
    # img = cv2.imread(image_path)
    # if img is None:
    #     raise FileNotFoundError(f"Image not found at path: {image_path}")

    # # Convert to grayscale
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Invert the image and apply a binary threshold.
    # Text becomes white (255) and background becomes black (0).
    # This helps in calculating the sum of pixels for projection.
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # 2. Find the best angle
    best_angle = 0.0
    max_score = -1.0
    h, w = thresh.shape[:2]
    center = (w // 2, h // 2)

    # Test a range of angles
    angles_to_test = cast(NDArray[np.float64], np.arange(min_angle, max_angle, step))

    angle: np.float64    
    for angle in angles_to_test:
        # Get the rotation matrix and apply the rotation
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(thresh, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

        # Calculate the "score" for this angle.
        # We sum the pixel values for each row and then sum the squares of these sums.
        # The angle that produces the sharpest horizontal lines will have the highest score.
        projection_scores = np.sum(rotated, axis=1) ** 2
        current_score = np.sum(projection_scores)

        if current_score > max_score:
            max_score = current_score
            best_angle = angle

    return best_angle

def process_file(ix: int, filefp: str, dest: str, skip_enhance:bool=False):
    if ix!=230:
        return

    print(ix, filefp)

    # Step 1: Open the image with Pillow to read metadata (like DPI)
    with Image.open(filefp) as pil_img:
        # Store original metadata
        original_info = cast(dict[str, Any], pil_img.info)

        # Step 2: Convert Pillow image to an OpenCV compatible format (NumPy array)
        # Pillow uses RGB, OpenCV uses BGR for color, so we convert if needed.
        # For grayscale, it's a direct conversion.
        opencv_img = np.array(pil_img)
        if pil_img.mode == 'RGB':
            opencv_img = cv2.cvtColor(opencv_img, cv2.COLOR_RGB2BGR)

    height, width = opencv_img.shape[:2]

    if ix%2 == 0:
        opencv_img = opencv_img[even_cropTop:height-even_cropBottom, even_cropLeft:width-even_cropRight]
    else:
        opencv_img = opencv_img[odd_cropTop:height-odd_cropBottom, odd_cropLeft:width-odd_cropRight]

    # Step 3: Find the skew angle using our function
    if ix==230:
        skew_angle = 0.6
    else:
        skew_angle = find_skew_angle(opencv_img)
    correction_angle = skew_angle
    print(f"🔍 Angle detected: {skew_angle:.2f}°. Applying {-skew_angle:.2f}° correction.")

    # Step 4: Rotate the original image to correct the skew
    h, w = opencv_img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, correction_angle, 1.0)

    # Use white as the border color to fill new areas
    # For grayscale this is 255, for color (BGR) it's (255, 255, 255)
    border_color = 255 if len(opencv_img.shape) == 2 else (255, 255, 255)
    
    corrected_opencv_img = cv2.warpAffine(
        opencv_img, M, (w, h), borderValue=border_color
    )
    #print("🔄 Image has been deskewed.")

    # Step 5: Convert the corrected OpenCV image back to Pillow format
    if pil_img.mode == 'RGB':
        # Convert BGR back to RGB for Pillow
        corrected_opencv_img = cv2.cvtColor(corrected_opencv_img, cv2.COLOR_BGR2RGB)
    
    corrected_pil_img = Image.fromarray(corrected_opencv_img)

    # Step 6: Save the corrected image using Pillow, preserving original metadata
    corrected_pil_img.save(dest, **original_info)
    #print(f"✅ Corrected image saved successfully as '{output_file}' with original metadata.")


def crop_and_resize(deskewed_img, target_width, target_height):
    return cv2.resize(deskewed_img, (target_width, target_height), interpolation=cv2.INTER_LANCZOS4)

def process_dir():
    os.makedirs(target, exist_ok=True)
    files = sorted(list(get_files(source, True)))
    for ix, filefp in enumerate(files):
        dest = filefp.replace(source, target)
        process_file(ix+1, filefp, dest)

if __name__ == '__main__':
    process_dir()

# 0,45°
#filefp = r"C:\PicturesODMisc\Aux frontières des mathématiques\Cropped\AFDM044.png"
#img = imread(filefp)
#angle = find_skew_angle(img)
#print("Angle:", angle)
