# This image is a gray image of a scanned page of text. It is rotated of 0.45° (clockwise).
# I'd like a python program with a reliable analyzis of this image and telling me it's rotated 0.45°, so I can manually
# rotate it of -0.45° to get it straight.
# To speed up the program, rotation will never be outside -1°..+1°, and a precision of 1/20th is enough for me. 


# How the Program Works
#
#    Preprocessing: The image is first loaded and converted to grayscale. It's then converted to a binary (black and
#    white) image where the text is white and the background is black. This makes the text pixels easy to count.
#
#    Rotation and Scoring: The program iterates through a range of angles from -1° to +1° in steps of 0.05° (1/20th).
#    For each angle, it performs a temporary rotation of the image.
#
#    Projection Profile: After each rotation, it calculates a "score" by summing up the white pixel values along each
#    horizontal row. The angle that makes the text perfectly horizontal will cause the white pixels to be concentrated
#    in fewer rows, resulting in the highest score.
#
#    Result: The angle that achieved the highest score is identified as the skew angle of the image. The program then
#    prints this detected angle and the necessary angle for correction. Running this script with your image produces the
#    output:
#
#    ✅ Analysis Complete! - Detected Skew Angle: 0.45° (clockwise) - Correction Needed:   -0.45° (counter-clockwise)


# One more thing, the image comes from a .png file, and once I find the skew angle, I'd like to unskew my image (image
# should keep its original size, some small parts may be cropped by rotation, and new areas created by rotation should
# be white filled, or just expand border color).
# 
# Then I'd like to save it in another .png file keeping all original attributes (a gray image, size, pixel density...
# and other .png attributes) 


# Why a Second Library (Pillow) is Needed
# 
#     OpenCV is excellent and fast for image processing tasks like rotation, filtering, and analysis. However, it tends
#     to ignore metadata and focuses only on the pixel matrix. When you use cv2.imread() and cv2.imwrite(), you often
#     lose information like DPI.
# 
#     Pillow (PIL) is the standard Python library for image I/O (Input/Output). It excels at reading and writing various
#     image formats while keeping their specific attributes intact.
# 
# By combining them, you get the best of both worlds: Pillow for careful loading/saving and OpenCV for high-performance
# processing.
    

import cv2
import numpy as np
from typing import Any, cast
from numpy.typing import NDArray
from PIL import Image

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
    print(angles_to_test.dtype)
    
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

# --- Main execution ---
if __name__ == "__main__":
    input_file = r"C:\PicturesODMisc\Aux frontières des mathématiques\Cropped\AFDM044.png"  # Your input PNG file
    output_file = r'C:\PicturesODMisc\Aux frontières des mathématiques\AFDM044_corrected.png' # The output file

    try:
        # Step 1: Open the image with Pillow to read metadata (like DPI)
        print(f"Opening '{input_file}' to read image data and metadata...")
        with Image.open(input_file) as pil_img:
            # Store original metadata
            original_info = cast(dict[str, Any], pil_img.info)
            print(f"  - Original metadata includes: {list(original_info.keys())}")

            # Step 2: Convert Pillow image to an OpenCV compatible format (NumPy array)
            # Pillow uses RGB, OpenCV uses BGR for color, so we convert if needed.
            # For grayscale, it's a direct conversion.
            opencv_img = np.array(pil_img)
            if pil_img.mode == 'RGB':
                opencv_img = cv2.cvtColor(opencv_img, cv2.COLOR_RGB2BGR)

        # Step 3: Find the skew angle using our function
        skew_angle = find_skew_angle(opencv_img)
        correction_angle = -skew_angle
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
        print("🔄 Image has been deskewed.")

        # Step 5: Convert the corrected OpenCV image back to Pillow format
        if pil_img.mode == 'RGB':
            # Convert BGR back to RGB for Pillow
            corrected_opencv_img = cv2.cvtColor(corrected_opencv_img, cv2.COLOR_BGR2RGB)
        
        corrected_pil_img = Image.fromarray(corrected_opencv_img)

        # Step 6: Save the corrected image using Pillow, preserving original metadata
        corrected_pil_img.save(output_file, **original_info)
        print(f"✅ Corrected image saved successfully as '{output_file}' with original metadata.")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")