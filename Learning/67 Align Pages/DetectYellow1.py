import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import scipy

img = mpimg.imread('Page11.png')
width = img.shape[1]
height = img.shape[0]

yellow = np.array([0.7921569, 0.6392157, 0.27058825])
yellow1 = np.array([0.7821569, 0.6292157, 0.26058825])

def dotdist(p1, p2):
    return np.linalg.norm(p2-p1)

dist = dotdist(yellow, yellow1)
print(dist)

# dcol=[]
# for col in range(width):
#     rowdist = [dotdist(img[row, col], yellow) for row in range(height)]
#     n = sum(1 if d<0.05 else 0 for d in rowdist)
#     dcol.append(n)
# print(dcol)

# plt.plot(dcol)
# plt.show()

drow=[]
for row in range(height):
    coldist = [dotdist(img[row, col], yellow) for col in range(width)]
    n = sum(1 if d<0.05 else 0 for d in coldist)
    drow.append(n)
print(drow)

plt.plot(drow)
plt.show()
