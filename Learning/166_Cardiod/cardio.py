# cardio.py
# Drawing a cardiod with Python and Matplotlib
#
# 2025-10-28    PV      First version

# I'd like a Python program drawing a cardiod using matplotlib. A cardioid is a series of straight lines between two
# points on a circle, one at angle theta, one at angle 2*theta, theta varying from 0 to 350 degrees by steps of 10
# degrees.
# 
# The program should show a visual image of the cardioid, and propose to export it as a PDF file 

import numpy as np
import matplotlib.pyplot as plt

print("Generating cardioid...")

# 1. Define angles in degrees and convert to radians
# np.arange(0, 360, 10) gives [0, 10, ..., 350]
theta_deg = np.arange(0, 360, 5)
theta_rad = np.radians(theta_deg)

# 2. Calculate coordinates for P1 (at theta) and P2 (at 2*theta)
# We assume a unit circle (radius = 1)
x1 = np.cos(theta_rad)
y1 = np.sin(theta_rad)

x2 = np.cos(2 * theta_rad)
y2 = np.sin(2 * theta_rad)

# 3. Set up the plot
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_aspect('equal') # Make the circle circular
ax.axis('off') # Hide the x and y axes
ax.set_title('Cardioid (Lines from $theta$ to $2*theta$)')

# 4. (Optional but nice) Draw the base circle
circle_theta_fine = np.linspace(0, 2 * np.pi, 200)
ax.plot(np.cos(circle_theta_fine), np.sin(circle_theta_fine), color='gray', linestyle='--', linewidth=0.8)

# 5. Draw the cardioid lines
for i in range(len(theta_rad)):
    # Plot a line from (x1[i], y1[i]) to (x2[i], y2[i])
    ax.plot([x1[i], x2[i]], [y1[i], y2[i]], color='blue', alpha=0.4, linewidth=0.7)

# 6. Save the output files
png_filename = 'cardioid_plot.png'
pdf_filename = 'cardioid_plot.pdf'

try:
    plt.savefig(png_filename, dpi=150, bbox_inches='tight')
    plt.savefig(pdf_filename, bbox_inches='tight')
    
    print(f"Successfully saved image to {png_filename}")
    print(f"Successfully saved PDF to {pdf_filename}")
    print("Plot generation complete.")

except Exception as e:
    print(f"Error saving files: {e}")

# Optionally view the result
plt.show()
