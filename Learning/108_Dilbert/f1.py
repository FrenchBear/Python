import numpy as np

def newprint(m: np.ndarray):
    s = m.shape
    for r in range(s[0]):
        print('[' if r == 0 else ' ', end='')
        for c in range(s[1]):
            print('[' + ','.join(map(str, m[r][c])) + ']', end='')
            if c < s[1]-1:
                print(' ', end='')
            else:
                print(']' if r == s[0]-1 else '')
    print()


rep = 3
img = np.array([[1, 2], [3, 4], [5, 6]])    # BW
img = np.array([[[1, 2, 3], [2, 3, 4]], [[3, 4, 5], [4, 5, 6]], [[5, 6, 7], [6, 7, 8]]])    # BW
newprint(img)


def test_1_3d():
    global img
    cols = np.repeat(img[:, 0, :].reshape(img.shape[0], 1, 3), rep, axis=1)
    img = np.insert(img, [0]*rep, cols, axis=1)
    return


def test_1_2d():
    global img
    c1 = img[:, 0]
    c2 = np.tile(c1.flatten(order='F'), rep)
    print(c2, end='\n\n')
    cols = c2.reshape((img.shape[0], rep, 3), order='F')
    newprint(cols)
    img = np.insert(img, [0]*rep, cols, axis=1)
    # newprint(img)


def test_2():   # Ok
    idx = [0]*rep
    col = np.array([7, 8, 9]*rep).reshape((3, rep), order='F')
    print(col)
    b = np.insert(img, idx, col, axis=1)
    print(b)


test_1_3d()
newprint(img)
