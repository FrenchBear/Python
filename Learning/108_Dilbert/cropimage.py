# cropimage.py
# Subroutine resizing a pic, either cropping borders or repeating tob/bottom/left/right row/column
#
# 2022-01-06    PV
# 2022-03-21    PV      Optimized insertions (removed loop), added BW version

import numpy as np


def crop_color_image(img: np.ndarray, inserttop: int, insertbottom: int, insertleft: int, insertright: int) -> np.ndarray:
    # Insert/delete left column duplicating existing column 0 rep times
    rep = insertleft
    if rep > 0:
        # for i in range(rep):
        #     img = np.insert(img, 0, img[:, 0, :], axis=1)
        cols = np.repeat(img[:, 0, :].reshape(img.shape[0], 1, 3), rep, axis=1)
        img = np.insert(img, [0]*rep, cols, axis=1)
    elif rep < 0:
        img = np.delete(img, range(-rep), axis=1)

    # Insert right column duplicating last column rep times
    rep = insertright
    if rep > 0:
        # for i in range(rep):
        #     img = np.insert(img, img.shape[1], img[:, -1, :], axis=1)
        cols = np.repeat(img[:, -1, :].reshape(img.shape[0], 1, 3), rep, axis=1)
        img = np.insert(img, [img.shape[1]]*rep, cols, axis=1)
    elif rep < 0:
        img = np.delete(img, range(img.shape[1]+rep, img.shape[1]), axis=1)

    # Insert top row duplicating existing row 0 rep times
    rep = inserttop
    if rep > 0:
        # for i in range(rep):
        #     img = np.insert(img, 0, img[0, :, :], axis=0)
        cols = np.repeat(img[0, :, :].reshape(1, img.shape[1], 3), rep, axis=0)
        img = np.insert(img, [0]*rep, cols, axis=0)
    elif rep < 0:
        img = np.delete(img, range(-rep), axis=0)

    # Insert bottom row duplicating last row rep times
    rep = insertbottom
    if rep > 0:
        # for i in range(rep):
        #     img = np.insert(img, img.shape[0], img[-1, :, :], axis=0)
        cols = np.repeat(img[-1, :, :].reshape(1, img.shape[1], 3), rep, axis=0)
        img = np.insert(img, [img.shape[0]]*rep, cols, axis=0)
    elif rep < 0:
        img = np.delete(img, range(img.shape[0]+rep, img.shape[0]), axis=0)

    return img


def crop_bw_image(img: np.ndarray, inserttop: int, insertbottom: int, insertleft: int, insertright: int) -> np.ndarray:
    # Insert/delete left column duplicating existing column 0 rep times
    rep = insertleft
    if rep > 0:
        cols = np.tile(img[:, 0], rep).reshape((img.shape[0], rep), order='F')
        img = np.insert(img, [0]*rep, cols, axis=1)
    elif rep < 0:
        img = np.delete(img, range(-rep), axis=1)

    # Insert right column duplicating last column rep times
    rep = insertright
    if rep > 0:
        cols = np.tile(img[:, -1], rep).reshape((img.shape[0], rep), order='F')
        img = np.insert(img, [img.shape[1]]*rep, cols, axis=1)
    elif rep < 0:
        img = np.delete(img, range(img.shape[1]+rep, img.shape[1]), axis=1)

    # Insert top row duplicating existing row 0 rep times
    rep = inserttop
    if rep > 0:
        img = np.insert(img, [0]*rep, img[0, :], axis=0)
    elif rep < 0:
        img = np.delete(img, range(-rep), axis=0)

    # Insert bottom row duplicating last row rep times
    rep = insertbottom
    if rep > 0:
        img = np.insert(img, [img.shape[0]]*rep, img[-1, :], axis=0)
    elif rep < 0:
        img = np.delete(img, range(img.shape[0]+rep, img.shape[0]), axis=0)

    return img


def crop_bw_image_white_borders(img: np.ndarray, inserttop: int, insertbottom: int, insertleft: int, insertright: int) -> np.ndarray:
    # Insert/delete left column duplicating existing column 0 rep times
    rep = insertleft
    if rep > 0:
        cols = np.full([img.shape[0], rep], 255, dtype=int)
        img = np.insert(img, [0]*rep, cols, axis=1)
    elif rep < 0:
        img = np.delete(img, range(-rep), axis=1)

    # Insert right column duplicating last column rep times
    rep = insertright
    if rep > 0:
        cols = np.full([img.shape[0], rep], 255, dtype=int)
        img = np.insert(img, [img.shape[1]]*rep, cols, axis=1)
    elif rep < 0:
        img = np.delete(img, range(img.shape[1]+rep, img.shape[1]), axis=1)

    # Insert top row duplicating existing row 0 rep times
    rep = inserttop
    if rep > 0:
        rows = np.full([rep, img.shape[1]], 255, dtype=int)
        img = np.insert(img, [0]*rep, rows, axis=0)
    elif rep < 0:
        img = np.delete(img, range(-rep), axis=0)

    # Insert bottom row duplicating last row rep times
    rep = insertbottom
    if rep > 0:
        rows = np.full([rep, img.shape[1]], 255, dtype=int)
        img = np.insert(img, [img.shape[0]]*rep, rows, axis=0)
    elif rep < 0:
        img = np.delete(img, range(img.shape[0]+rep, img.shape[0]), axis=0)

    return img
