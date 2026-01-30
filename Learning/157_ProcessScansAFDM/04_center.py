# center.py
# Shift page contents to have aligned pages
# See info.txt for details
#
# 2025-09-20    PV


import numpy as np
from PIL import Image
from pathlib import Path
from tqdm import tqdm
from typing import Optional, Tuple, Dict, cast
from numpy.typing import NDArray

# --- CONFIGURATION ---

# 1. File and Folder Paths
# Use raw strings (r'...') for Windows paths to avoid issues with backslashes.
SOURCE_FOLDER = Path(r'C:\PicturesODMisc\Aux frontières des mathématiques\Cropped,Deskewed')
DESTINATION_FOLDER = Path(r'C:\PicturesODMisc\Aux frontières des mathématiques\Centered')
FILE_PREFIX = 'AFDM'

# 2. Page Range to Process
# Skip the first two and last two pages as requested.
START_PAGE = 3
END_PAGE = 238

# 3. Image Analysis Parameters
# Pixels with a value below this are considered "black" text. Adjust if needed.
BLACK_THRESHOLD = 200 

# 4. Global Bounding Boxes (x, y, width, height)
# These are the large areas to search within for actual content.
GLOBAL_BOUNDING_BOXES = {
    'even': {
        'title':  (822, 124, 1588, 188),
        'body':   (238, 468, 2765, 4486),
        'number': (1450, 4959, 299, 174)
    },
    'odd': {
        'title':  (563, 119, 2166, 144),
        'body':   (259, 446, 2803, 4468),
        'number': (1513, 4951, 280, 177)
    }
}

# 5. Alignment Target Coordinates
# These are the goals for the final alignment.
TARGETS = {
    'number_center': (1650, 5100),
    'title_center':  (1650, 272),
    'body_left_margin': 395
}

# --- TYPE HINTS for clarity ---
BoundingBox = tuple[int, int, int, int]


def find_actual_bounding_box(
    image_array: NDArray[np.uint8], 
    global_bbox: BoundingBox
) -> BoundingBox | None:
    """
    Searches within a global bounding box for the tightest box around non-white pixels.

    Args:
        image_array: The entire image as a NumPy array.
        global_bbox: The (x, y, w, h) tuple defining the area to search.

    Returns:
        The (x, y, w, h) of the actual content, or None if no content is found.
    """
    x, y, w, h = global_bbox
    
    # Crop the image array to the region of interest (ROI)
    roi = image_array[y : y + h, x : x + w]

    # Find coordinates of all pixels darker than the threshold
    black_pixels_coords = np.where(roi < BLACK_THRESHOLD)

    if not black_pixels_coords[0].size:
        # No black pixels found in this ROI
        return None

    # Get the min/max coordinates of the black pixels within the ROI
    y_min_roi, y_max_roi = np.min(black_pixels_coords[0]), np.max(black_pixels_coords[0])
    x_min_roi, x_max_roi = np.min(black_pixels_coords[1]), np.max(black_pixels_coords[1])

    # Calculate the actual bounding box relative to the full image
    actual_x = x + x_min_roi
    actual_y = y + y_min_roi
    actual_w = x_max_roi - x_min_roi + 1
    actual_h = y_max_roi - y_min_roi + 1

    return cast(BoundingBox, (actual_x, actual_y, actual_w, actual_h))


def calculate_shift(
    bboxes: dict[str, BoundingBox | None], 
    image_width: int
) -> tuple[int, int]:
    """
    Calculates the required (dx, dy) shift based on a prioritized list of rules.

    Args:
        bboxes: A dictionary containing the found bounding boxes for 'title', 'body', 'number'.
        image_width: The width of the source image.
        
    Returns:
        A tuple (dx, dy) representing the horizontal and vertical shift.
    """
    # Rule 1: Align based on the page number (highest priority)
    if bboxes.get('number'):
        x, y, w, h = bboxes['number']       # type: ignore
        current_center_x = x + w / 2
        current_center_y = y + h / 2
        dx = TARGETS['number_center'][0] - current_center_x
        dy = TARGETS['number_center'][1] - current_center_y
        return int(round(dx)), int(round(dy))

    # Rule 2: Align based on the title (second priority)
    if bboxes.get('title'):
        x, y, w, h = bboxes['title']       # type: ignore
        current_center_x = x + w / 2
        current_center_y = y + h / 2
        dx = TARGETS['title_center'][0] - current_center_x
        dy = TARGETS['title_center'][1] - current_center_y
        return int(round(dx)), int(round(dy))

    # Rule 3: Align based on the body text's left margin (lowest priority)
    if bboxes.get('body'):
        x, _, _, _ = bboxes['body']       # type: ignore
        current_left_margin = x
        dx = TARGETS['body_left_margin'] - current_left_margin
        # No vertical hint for the body, so dy is 0
        return int(round(dx)), 0

    # If no elements are found, no shift is applied
    return 0, 0


def process_image(file_path: Path):
    """
    Main processing logic for a single image file.
    """
    try:
        img = Image.open(file_path).convert('L') # 'L' is for 8-bit grayscale
    except FileNotFoundError:
        print(f"\nWarning: File not found, skipping: {file_path.name}")
        return
    except Exception as e:
        print(f"\nError opening {file_path.name}: {e}")
        return

    # Convert image to NumPy array for fast processing
    image_array = np.array(img)
    
    # Determine if the page is odd or even to use the correct global boxes
    page_number = int(file_path.stem.replace(FILE_PREFIX, ''))
    page_type = 'odd' if page_number % 2 != 0 else 'even'
    
    # Find the actual bounding box for each element
    element_bboxes = {}
    for element, global_bbox in GLOBAL_BOUNDING_BOXES[page_type].items():
        element_bboxes[element] = find_actual_bounding_box(image_array, global_bbox)

    # If the page is completely blank in the specified regions, skip it
    if all(bbox is None for bbox in element_bboxes.values()):
        print(f"\nNote: Page {page_number} appears blank, skipping alignment.")
        # Optionally, you could just copy it to the destination
        # img.save(DESTINATION_FOLDER / file_path.name, dpi=(600, 600))
        return

    # Calculate the necessary shift based on the found elements
    dx, dy = calculate_shift(element_bboxes, img.width)

    if dx == 0 and dy == 0:
        print(f"\nNote: Page {page_number} is already aligned, copying as is.")
        # Save the original image with correct DPI
        img.save(DESTINATION_FOLDER / file_path.name, dpi=(600, 600))
        return

    # Create a new blank (white) image of the same size
    # The new areas will be white by default
    new_img = Image.new('L', img.size, 255)

    # Paste the original image onto the new canvas at the shifted position
    new_img.paste(img, (dx, dy))

    # Save the resulting image with 600 DPI
    output_path = DESTINATION_FOLDER / file_path.name
    new_img.save(output_path, dpi=(600, 600))


def main():
    """
    Main function to orchestrate the alignment process.
    """
    print("--- Page Alignment Script ---")
    
    # Validate source folder exists
    if not SOURCE_FOLDER.is_dir():
        print(f"Error: Source folder not found at '{SOURCE_FOLDER}'")
        return

    # Create destination folder if it doesn't exist
    DESTINATION_FOLDER.mkdir(parents=True, exist_ok=True)
    print(f"Source:      {SOURCE_FOLDER}")
    print(f"Destination: {DESTINATION_FOLDER}\n")

    # Generate the list of pages to process
    pages_to_process = range(START_PAGE, END_PAGE + 1)
    
    # Process each file with a progress bar
    for page_num in tqdm(pages_to_process, desc="Aligning Pages"):
        filename = f"{FILE_PREFIX}{page_num:03d}.png"
        file_path = SOURCE_FOLDER / filename
        process_image(file_path)

    print("\n✅ Alignment process completed successfully!")


if __name__ == "__main__":
   main()

# page_num = 5
# filename = f"{FILE_PREFIX}{page_num:03d}.png"
# file_path = SOURCE_FOLDER / filename
# process_image(file_path)
