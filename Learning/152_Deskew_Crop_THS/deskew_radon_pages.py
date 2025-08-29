# deskew_radon_pages.py
#
# 2025-08-28    PV


# Gemini query
# I have several scanned PNG images of book covers, and there are two elements to improve:
# - Due to book placement on scanner, cover image borders may not be perfectly vertical and horizontal, but sometimes
#   slanted a bit.
# - Scanned area is a a bit larger than book cover itself, resulting in black (actually very dark, not necessarily
#   black) borders
#
# I'd like to write a Python program, doing image processing using typical libraries such as matplotlib.image to
# read/write image files into numpy arrays, and numpy to do efficient image analysis (other libraries may be used).
# - First step should be image deskewing, so that text and other vertical/horizontal elements of the cover are the more
#   vertical and horizontal possible
# - Second step after deskewing is image cropping to a target fixed size of 4000 pixels wide by 5650 pixels height,
#   removing dark borders of cover image to keep only the best part of cover image.

# Gemini answer
# Code for Deskewing with Radon Transform
#
# Here's the Python code for deskewing images using the Radon transform, which is a powerful method for detecting the
# dominant angle in an image. This approach is generally more robust than the Hough transform for this specific task.
# The code uses scikit-image for the Radon transform and OpenCV for image manipulation and rotation.
#
# You'll need to install the necessary libraries first: pip install scikit-image opencv-python numpy

import os
import cv2
import numpy as np
from skimage.transform import radon, rotate
from skimage.io import imread, imsave
from skimage.color import rgb2gray
from skimage.transform import resize
from common_fs import get_all_files
from concurrent.futures import ProcessPoolExecutor

def find_skew_angle(image):
    """
    Finds the skew angle of an image using the Radon transform.
    """

    # Resize image to speed up processing
    image = resize(image, (image.shape[0] // 8, image.shape[1] // 8), anti_aliasing=True)

    # Convert to grayscale
    gray = rgb2gray(image)

    # Binarize the image to simplify the detection of lines
    # This helps the Radon transform focus on the main structures.
    # We use a threshold of 0.5 (or any value that separates the text/lines from background)
    binary = gray > np.mean(gray)

    # Compute the Radon transform
    # The output is an array of projections at different angles.
    # We look for the angle with the highest variance, as it corresponds to the main lines.
    theta = np.linspace(-5., 5., max(image.shape), endpoint=False)
    sinogram = radon(binary, theta=theta, circle=False)

    # Find the angle with the maximum variance in its projection
    # This angle should correspond to the skew of the text/lines
    variance = np.var(sinogram, axis=0)
    angle = theta[np.argmax(variance)]

    angle = angle if angle < 90 else angle - 180
    # if abs(angle) >= 5:
    #     angle = 0.0
    return angle

def deskew_image_radon(image_path):
    """
    Loads an image, deskews it using Radon transform, and returns the result.
    """
    img = imread(image_path)

    # Find the skew angle
    angle = find_skew_angle(img)
    print(f"Detected skew angle: {angle:.2f} degrees")

    # Rotate the image by the detected skew angle
    # The rotate function handles the transformation and resizing
    rotated_img = rotate(img, -angle, resize=True, mode='edge')

    # Convert back to uint8 format for OpenCV compatibility if needed
    rotated_img = (rotated_img * 255).astype(np.uint8)

    return rotated_img

def crop_and_resize(deskewed_img, target_width=3900, target_height=5600):
    return cv2.resize(deskewed_img, (target_width, target_height), interpolation=cv2.INTER_LANCZOS4)


source = r"C:\PicturesODMisc\THS\Scans"
target = r"C:\PicturesODMisc\THS\RR2"

def process_file(filefp: str):
    try:
        print(filefp)
        deskewed_image = deskew_image_radon(filefp)
        final_image = crop_and_resize(deskewed_image)
        dest = filefp.replace(source, target)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        imsave(dest, final_image)
    except Exception as e:
        return f"Error processing {filefp}: {e}"


if __name__ == '__main__':
    files = list(get_all_files(source))
    with ProcessPoolExecutor(max_workers=10) as executor:
        results = executor.map(process_file, files)
        for result in results:
            print(result)
