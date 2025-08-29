# deskew_crop_ths.py
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
# Overview
# 
# To process the scanned book covers, you'll need a Python program that first deskews the images and then crops them to
# a fixed size, removing the dark borders. We can use libraries like NumPy for array manipulation, OpenCV for image
# processing, and scikit-image for advanced transformations.
# 
# Step 1: Image Deskewing
# 
# Deskewing involves rotating the image to align the main elements (like text and the book's spine) with the horizontal
# and vertical axes. A common approach is to use the Hough transform to detect lines in the image and calculate the
# average angle of these lines.
# 
#     Read the image: Load the PNG image into a NumPy array.
# 
#     Convert to grayscale: Deskewing algorithms work best on single-channel (grayscale) images.
# 
#     Detect edges: Apply a Canny edge detector to find the prominent lines in the image. This helps the Hough transform focus on the most important features.
# 
#     Find the rotation angle:
# 
#         Use the Hough Line Transform to detect all the prominent lines in the image.
# 
#         Calculate the angle of each line.
# 
#         Create a histogram of the angles to find the most frequent angle, which represents the skew.
# 
#         Alternatively, you can use a more robust method like Radon transform which is specifically designed for this kind of problem. Scikit-image provides a radon function which can be used to determine the angle of the main lines in the image.
# 
#     Rotate the image: Rotate the image by the negative of the detected angle. You can use OpenCV's warpAffine function for this. This step ensures that the book cover is properly aligned.
# 
# Step 2: Image Cropping
# 
# After deskewing, the image will have some empty black space around the edges from the rotation. The next step is to
# crop the image to the target size of 4000x5650 pixels while removing the dark borders.
# 
#     Find the bounding box: To identify the actual book cover area, you'll need to find the boundaries of the non-dark pixels.
# 
#         Convert the deskewed image back to grayscale if it isn't already.
# 
#         Apply a binary threshold to the image to separate the dark background from the book cover. All pixels above a certain brightness threshold become white, and all below become black.
# 
#         Find the coordinates of the minimum and maximum rows and columns that contain white pixels. This gives you the bounding box of the book cover.
# 
#     Crop the image:
# 
#         Use the bounding box coordinates to crop the original deskewed image, keeping only the book cover area.
# 
#     Resize to fixed dimensions:
# 
#         Once cropped, the image may not be exactly 4000x5650 pixels. Use OpenCV's resize function to scale the cropped image to the target dimensions. You can choose a suitable interpolation method like cv2.INTER_AREA for shrinking or cv2.INTER_CUBIC for enlarging.


import cv2
import numpy as np

def deskew_and_crop(image_path, target_width=4000, target_height=5650):
    img = cv2.imread(image_path)
    
    # 1. Deskewing
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)
    
    if lines is not None:
        angles = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
            angles.append(angle)
        
        median_angle = np.median(angles) if angles else 0
        
        (h, w) = img.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, median_angle, 1.0)
        deskewed_img = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    else:
        deskewed_img = img

    # 2. Cropping
    gray_deskewed = cv2.cvtColor(deskewed_img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray_deskewed, 25, 255, cv2.THRESH_BINARY)
    
    coords = cv2.findNonZero(thresh)
    if coords is not None:
        x, y, w, h = cv2.boundingRect(coords)
        cropped_img = deskewed_img[y:y+h, x:x+w]
        
        final_img = cv2.resize(cropped_img, (target_width, target_height), interpolation=cv2.INTER_AREA)
    else:
        final_img = cv2.resize(deskewed_img, (target_width, target_height), interpolation=cv2.INTER_AREA)
    
    return final_img

# Example usage:
processed_image = deskew_and_crop(r"C:\PicturesODMisc\THS\Couvertures\2 redressées\THS01.png")
cv2.imwrite(r"C:\PicturesODMisc\THS\Couvertures\3 recadrées\THS01.png", processed_image)
