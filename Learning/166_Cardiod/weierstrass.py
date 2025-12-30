# weierstrass.py
# Drawing weierstrass function with Python and Matplotlib
#
# 2025-10-29    PV      First version

# I'd like a Python program drawing 4 versions of Weierstrass function using matplotlib.
# The final image should be divided in four equal quadrants each cone containing a variant.
#
# Weiesrstrass function uses three parameters, a, b and nmax:
# - a is a real number between 0 and 1
# - b is an odd integer such as a*b>1+(3π/2)
# - nmax is an integer>=0
# defined as f[a,b,nmax](x) = sum(n=0..nmax, a^n * cos(b^n *π*x)
#
# Typically this function should be drawn on x scale from 0 to 2, and y scale from -2 to 2, using the same scale on both
# axes, and both axes visible, y axis drawn at x=0, and x axis drawn at y=0, with numerical labels at each integer
# value.
#
# At the beginning of the program, it should be possible to configure a, b and nmax for each quadrant.

import numpy as np
import matplotlib.pyplot as plt

def weierstrass(x: np.ndarray, a: float, b: int, nmax: int) -> np.ndarray:
    """
    Calculates the Weierstrass function for a given x.
    f(x) = sum(n=0..nmax, a^n * cos(b^n * π * x))
    """
    f_x = np.zeros_like(x, dtype=float)
    for n in range(nmax + 1):
        f_x += (a**n) * np.cos((b**n) * np.pi * x)
    return f_x

# --- Configuration for each quadrant ---
# List of tuples (a, b, nmax) for the 4 quadrants
quadrant_params = [
    (0.5, 3, 0),  # Quadrant 1 (Top-Left)
    (0.5, 3, 2),  # Quadrant 2 (Top-Right)
    (0.5, 3, 4),  # Quadrant 3 (Bottom-Left)
    (0.5, 3, 6)   # Quadrant 4 (Bottom-Right)
]

# --- Generate x values ---
x_values = np.linspace(0, 2, 10000) # Increased resolution to avoid aliasing

# --- Create the figure and 2x2 subplots ---
fig, axes = plt.subplots(2, 2, figsize=(12, 12))
fig.suptitle("Weierstrass Function Variants W[a,b,nmax](x) = sum(n=0..nmax, a^n * cos(b^n *π*x)", fontsize=16)

# --- Plotting function for each quadrant ---
def plot_weierstrass_quadrant(ax, x_vals, a, b, nmax, title):
    y_values = weierstrass(x_vals, a, b, nmax)
    ax.plot(x_vals, y_values, color='blue', linewidth=1)

    # Set x and y limits and aspect ratio
    ax.set_xlim(0, 2)
    ax.set_ylim(-2, 2)
    #ax.set_aspect('equal', adjustable='box') # Same scale on both axes

    # Draw axes at x=0 and y=0
    ax.axhline(0, color='black', linewidth=0.7) # X-axis
    ax.axvline(0, color='black', linewidth=0.7) # Y-axis

    # Set integer ticks
    ax.set_xticks(np.arange(0, 3, 1))
    ax.set_yticks(np.arange(-2, 3, 1))

    # Add grid for better readability
    ax.grid(True, linestyle='--', alpha=0.6)

    ax.set_title(title, fontsize=10)

# --- Apply plotting to each quadrant ---
for ax, (a, b, nmax) in zip(axes.flat, quadrant_params):
    plot_weierstrass_quadrant(ax, x_values, a, b, nmax, f'a={a}, b={b}, nmax={nmax}')

plt.tight_layout(rect=(0, 0.03, 1, 0.96)) # Adjust layout to prevent title overlap
#plt.savefig('weierstrass_functions.png', dpi=300)
plt.show()
