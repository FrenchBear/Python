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

def weierstrass(x, a, b, nmax):
    """
    Calculates the Weierstrass function for a given x.
    f(x) = sum(n=0..nmax, a^n * cos(b^n * π * x))
    """
    f_x = np.zeros_like(x, dtype=float)
    for n in range(nmax + 1):
        f_x += (a**n) * np.cos((b**n) * np.pi * x)
    return f_x

# --- Configuration for each quadrant ---
# Quadrant 1 (Top-Left)
a1, b1, nmax1 = 0.5, 7, 5
# Quadrant 2 (Top-Right)
a2, b2, nmax2 = 0.8, 9, 3
# Quadrant 3 (Bottom-Left)
a3, b3, nmax3 = 0.4, 5, 8
# Quadrant 4 (Bottom-Right)
a4, b4, nmax4 = 0.6, 11, 4

# variation of nmax
a1, b1, nmax1 = 0.5, 3, 0
a2, b2, nmax2 = 0.5, 3, 2
a3, b3, nmax3 = 0.5, 3, 4
a4, b4, nmax4 = 0.5, 3, 6


# --- Generate x values ---
x_values = np.linspace(0, 2, 1000) # 1000 points between 0 and 2

# --- Create the figure and 2x2 subplots ---
fig, axes = plt.subplots(2, 2, figsize=(12, 12))
fig.suptitle("Weierstrass Function Variants W[a,b,nmax](x) = sum(n=0..nmax, a^n * cos(b^n *π*x)", fontsize=16)

# --- Plotting function for each quadrant ---
def plot_weierstrass_quadrant(ax, a, b, nmax, title):
    y_values = weierstrass(x_values, a, b, nmax)
    ax.plot(x_values, y_values, color='blue', linewidth=1)

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
plot_weierstrass_quadrant(axes[0, 0], a1, b1, nmax1, f'a={a1}, b={b1}, nmax={nmax1}')
plot_weierstrass_quadrant(axes[0, 1], a2, b2, nmax2, f'a={a2}, b={b2}, nmax={nmax2}')
plot_weierstrass_quadrant(axes[1, 0], a3, b3, nmax3, f'a={a3}, b={b3}, nmax={nmax3}')
plot_weierstrass_quadrant(axes[1, 1], a4, b4, nmax4, f'a={a4}, b={b4}, nmax={nmax4}')

plt.tight_layout(rect=(0, 0.03, 1, 0.96)) # Adjust layout to prevent title overlap
#plt.savefig('weierstrass_functions.png', dpi=300)
plt.show()
