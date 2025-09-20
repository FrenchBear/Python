# supperpose.py
#
# 2025-09-20    PV

# I have a folder containing 240 gray scale PNG pictures, all the same size named AFDM###.png where ### is a three-digit
# number from 001 to 240. These pages have a near white background, and black text over it.
# I'd like a Python program to combine all even pages into one page, and all odd pages into one page (and save both
# combined pages into a PNG file).
# The combined page should be the visual superposition of the pages to combine, a pixel of the combination pic should
# be the darkest of all images to combine. The combination function should be something like min, or a normalized
# product to remain in 0-255 range, I don't know which one gives the best visual result, so I'll try both, or any other
# function you map provide.

import os
import numpy as np
from PIL import Image

# --- Configuration ---
# Use a raw string (r'...') to handle backslashes in Windows paths.
# Please ensure this path is correct.
IMAGE_FOLDER = r'C:\PicturesODMisc\Aux frontières des mathématiques\Cropped,Deskewed'
FILE_PREFIX = 'AFDM'
TOTAL_IMAGES = 240
OUTPUT_ODD_FILENAME =  r'C:\PicturesODMisc\Aux frontières des mathématiques\combined_odd_pages.png'
OUTPUT_EVEN_FILENAME = r'C:\PicturesODMisc\Aux frontières des mathématiques\combined_even_pages.png'

def combine_images(file_paths, folder, method='min'):
    """
    Combines a list of images using a specified method.

    Args:
        file_paths (list): A list of image filenames.
        folder (str): The path to the folder containing the images.
        method (str): The combination method ('min' or 'product').

    Returns:
        PIL.Image.Image or None: The combined image, or None if an error occurs.
    """
    if not file_paths:
        print("Warning: No files provided to combine.")
        return None

    print(f"Processing {len(file_paths)} images with the '{method}' method...")

    # Initialize with the first image
    try:
        first_image_path = os.path.join(folder, file_paths[0])
        # 'L' mode is for 8-bit grayscale.
        base_image = Image.open(first_image_path).convert('L')
        # Use float32 for calculations to prevent overflow/rounding issues.
        combined_array = np.array(base_image, dtype=np.float32)
    except FileNotFoundError:
        print(f"Error: The first image was not found at {first_image_path}. Aborting.")
        return None

    # Loop through the rest of the images and combine them
    for filename in file_paths[1:]:
        image_path = os.path.join(folder, filename)
        try:
            img = Image.open(image_path).convert('L')
            img_array = np.array(img, dtype=np.float32)

            if method == 'min':
                # Takes the element-wise minimum. This is the "darkest pixel" approach.
                combined_array = np.minimum(combined_array, img_array)
            elif method == 'product':
                # Normalizes to [0, 1], multiplies, then scales back to [0, 255].
                # This tends to make the result very dark.
                combined_array = (combined_array / 255.0) * (img_array / 255.0) * 255.0
            else:
                raise ValueError("Unsupported combination method. Use 'min' or 'product'.")

        except FileNotFoundError:
            print(f"Warning: Skipping missing file: {image_path}")
        except Exception as e:
            print(f"An error occurred while processing {image_path}: {e}")

    # Ensure all values are within the valid 0-255 range for an image
    combined_array = np.clip(combined_array, 0, 255)
    
    # Convert the final array back to an 8-bit integer image
    final_image = Image.fromarray(combined_array.astype(np.uint8))
    return final_image

if __name__ == "__main__":
    if not os.path.isdir(IMAGE_FOLDER):
        print(f"Error: The specified folder does not exist: {IMAGE_FOLDER}")
    else:
        # 1. Create lists of odd and even filenames, ignoring first 2 pages and last 2 pages
        odd_files = [f"{FILE_PREFIX}{i:03d}.png" for i in range(3, TOTAL_IMAGES - 1) if i % 2 != 0]
        even_files = [f"{FILE_PREFIX}{i:03d}.png" for i in range(3, TOTAL_IMAGES - 1) if i % 2 == 0]

        # 2. Combine odd pages
        print("--- Combining Odd Pages ---")
        combined_odd_image = combine_images(odd_files, IMAGE_FOLDER, method='min')
        if combined_odd_image:
            combined_odd_image.save(OUTPUT_ODD_FILENAME)
            print(f"✅ Successfully saved combined odd pages to: {OUTPUT_ODD_FILENAME}\n")

        # 3. Combine even pages
        print("--- Combining Even Pages ---")
        combined_even_image = combine_images(even_files, IMAGE_FOLDER, method='min')
        if combined_even_image:
            combined_even_image.save(OUTPUT_EVEN_FILENAME)
            print(f"✅ Successfully saved combined even pages to: {OUTPUT_EVEN_FILENAME}\n")

        print("All tasks completed.")