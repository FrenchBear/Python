# deskew_radon.py
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

import cv2
import numpy as np
from skimage.transform import radon, rotate
from skimage.io import imread, imsave
from skimage.color import rgb2gray
from skimage.transform import resize
from common_fs import get_files


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
    theta = np.linspace(0., 180., max(image.shape), endpoint=False)
    sinogram = radon(binary, theta=theta, circle=False)

    # Find the angle with the maximum variance in its projection
    # This angle should correspond to the skew of the text/lines
    variance = np.var(sinogram, axis=0)
    angle = theta[np.argmax(variance)]

    angle = angle if angle < 90 else angle - 180
    if abs(angle) >= 5:
        angle = 0.0
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

def crop_and_resize(deskewed_img, target_width=4000, target_height=5650):
    """
    Crops the deskewed image to remove borders and resizes it to the target dimensions.
    """

    # Convert to grayscale to find the non-black content
    gray = cv2.cvtColor(deskewed_img, cv2.COLOR_RGB2GRAY)
    # cv2.imwrite(r"C:\PicturesODMisc\THS\Couvertures\3 recadrées\THS01Gray.png", gray)

    # Threshold to create a binary image (dark background vs. bright foreground)
    _, thresh = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY)
    # cv2.imwrite(r"C:\PicturesODMisc\THS\Couvertures\3 recadrées\THS01Thresh.png", thresh)

    # Find the coordinates of the non-zero (white) pixels
    coords = cv2.findNonZero(thresh)
    if coords is not None:
        x, y, w, h = cv2.boundingRect(coords)
        # crop fuzzy borders
        delta = 20
        x += delta
        y += delta
        w -= 2 * delta
        h -= 2 * delta
        cropped_img = deskewed_img[y:y + h, x:x + w]

        # Resize to the final target dimensions
        final_img = cv2.resize(cropped_img, (target_width, target_height), interpolation=cv2.INTER_AREA)
        return final_img

    # If no content is found, just resize the whole image
    return cv2.resize(deskewed_img, (target_width, target_height), interpolation=cv2.INTER_AREA)


source = r"C:\PicturesODMisc\THS\Couvertures\2 redressées"
target = r"C:\PicturesODMisc\THS\Couvertures\3 recadrées"

for filefp in get_files(source, True):
    print(filefp)
    # Step 1: Deskew the image
    deskewed_image = deskew_image_radon(filefp)

    # Step 2: Crop and resize the deskewed image
    final_image = crop_and_resize(deskewed_image)

    # Step 3: Save the final image
    filename = filefp.split("\\")[-1]
    #cv2.imwrite(f"{target}\\{filename}", final_image)
    imsave(f"{target}\\{filename}", final_image)
