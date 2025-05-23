import numpy as np
from skimage.feature import canny                               # type: ignore
from skimage.transform import hough_line, hough_line_peaks      # type: ignore
from skimage import io                                          # type: ignore
from skimage.color import rgb2gray                              # type: ignore

from typing import Any, Optional


def _get_max_freq_elem(peaks: list[int]) -> list[float]:
    freqs: dict[float, int] = {}
    for peak in peaks:
        if peak in freqs:
            freqs[peak] += 1
        else:
            freqs[peak] = 1

    sorted_keys = sorted(freqs, key=freqs.get, reverse=True)        # type: ignore
    max_freq = freqs[sorted_keys[0]]

    max_arr = []
    for sorted_key in sorted_keys:
        if freqs[sorted_key] == max_freq:
            max_arr.append(sorted_key)

    return max_arr

def _compare_sum(value: float) -> bool:
    return 44 <= value <= 46

def _calculate_deviation(angle: float) -> float:

    angle_in_degrees = np.abs(angle)
    deviation = np.abs(np.pi / 4 - angle_in_degrees)

    return deviation

def determine_skew_dev(  # pylint: disable=too-many-locals
        image: np.ndarray, sigma: float = 3.0, num_peaks: int = 20
) -> tuple[Optional[float], Any, Any, Optional[tuple[Any, Any, Any]]]:
    img = image
    edges = canny(img, sigma=sigma)
    out, angles, distances = hough_line(edges)

    _, angles_peaks, _ = hough_line_peaks(out, angles, distances, num_peaks=num_peaks)

    absolute_deviations = [_calculate_deviation(k) for k in angles_peaks]
    average_deviation = np.mean(np.rad2deg(absolute_deviations))
    angles_peaks_degree = [np.rad2deg(x) for x in angles_peaks if -2<=np.rad2deg(x)<=2]

    bin_0_45 = []
    bin_45_90 = []
    bin_0_45n = []
    bin_45_90n = []

    angle: float
    for angle in angles_peaks_degree:

        deviation_sum = int(90 - angle + average_deviation)
        if _compare_sum(deviation_sum):
            bin_45_90.append(angle)
            continue

        deviation_sum = int(angle + average_deviation)
        if _compare_sum(deviation_sum):
            bin_0_45.append(angle)
            continue

        deviation_sum = int(-angle + average_deviation)
        if _compare_sum(deviation_sum):
            bin_0_45n.append(angle)
            continue

        deviation_sum = int(90 + angle + average_deviation)
        if _compare_sum(deviation_sum):
            bin_45_90n.append(angle)

    anglesll:list[list[float]] = [bin_0_45, bin_45_90, bin_0_45n, bin_45_90n]
    nb_angles_max = 0
    max_angle_index = -1
    for angle_index, anglelist in enumerate(anglesll):
        nb_angles = len(anglelist)
        if nb_angles > nb_angles_max:
            nb_angles_max = nb_angles
            max_angle_index = angle_index

    if nb_angles_max:
        ans_arr = _get_max_freq_elem(angles[max_angle_index])
        a = float(np.mean(ans_arr))
    elif angles_peaks_degree:
        ans_arr = _get_max_freq_elem(angles_peaks_degree)
        a = float(np.mean(ans_arr))
    else:
        return None, angles, average_deviation, (out, angles, distances)
    
    return a, None,None,None

    if 0 <= angle <= 90:
        rot_angle = angle - 90
    elif -45 <= angle < 0:
        rot_angle = angle - 90
    elif -90 <= angle < -45:
        rot_angle = 90 + angle

    return rot_angle, angles, average_deviation, (out, angles, distances)


def determine_skew(image: np.ndarray, sigma: float = 3.0, num_peaks: int = 20) -> Optional[float]:
    """
    Calculates skew angle

    Return None if no skew will be found
    """
    angle, _, _, _ = determine_skew_dev(image, sigma=sigma, num_peaks=num_peaks)
    return angle



source = r'C:\Scans\THS23\2 Crop\THS23-027.png'

image = io.imread(source)
grayscale = rgb2gray(image)
angle = determine_skew(grayscale)
print(angle)
