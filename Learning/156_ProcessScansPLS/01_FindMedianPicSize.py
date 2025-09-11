# 01_FindMedianPicSize.py
# I'd like a Python program to find median width and height in pixels of a series of images in a given folder
#
# 2025-09-11    PV


import os
from PIL import Image

def find_median_pic_size(folder_path: str) -> tuple[int, int]:
    """
    Finds the median width and height in pixels of a series of images in a given folder.

    Args:
        folder_path (str): The path to the folder containing the images.

    Returns:
        tuple: A tuple containing the median width and median height, or (None, None)
               if no images are found or an error occurs.
    """
    widths: list[int] = []
    heights: list[int] = []

    if not os.path.isdir(folder_path):
        print(f"Error: Folder not found at '{folder_path}'")
        return 0, 0

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            try:
                with Image.open(file_path) as img:
                    width, height = img.size
                    widths.append(width)
                    heights.append(height)
            except Exception as e:
                print(f"Could not process '{filename}': {e}")

    if not widths:
        print("No images found or processed in the folder.")
        return 0, 0

    widths.sort()
    heights.sort()

    median_width = calculate_median(widths)
    median_height = calculate_median(heights)

    return median_width, median_height

def calculate_median(data: list[int]) -> int:
    """Calculates the median of a sorted list of numbers."""
    n = len(data)
    if n % 2 == 1:
        return data[n // 2]
    else:
        mid1 = data[n // 2 - 1]
        mid2 = data[n // 2]
        return int((mid1 + mid2) / 2)

if __name__ == "__main__":
    # Example usage:
    # Replace 'path/to/your/image/folder' with the actual path to your image folder
    #image_folder = input("Enter the path to the image folder: ")
    image_folder = r"D:\Pierre\OneDrive\PicturesODMisc\PLS573\Originaux"
    median_w, median_h = find_median_pic_size(image_folder)
    print('w:', int(median_w), '  h:', int(median_h))
