# Import NumPy and Matplotlib
import numpy as np
import matplotlib.pyplot as plt

# Create an array
points = np.arange(-5, 5, 0.01)

# Make a meshgrid
xs, ys = np.meshgrid(points, points)
#z = np.sqrt(xs ** 2 + ys ** 2)
#z=np.abs(xs)+np.abs(ys)
z=xs*ys*ys

# Display the image on the axes
plt.imshow(z, cmap=plt.cm.gray)

# Draw a color bar
plt.colorbar()

# Show the plot
plt.show()
