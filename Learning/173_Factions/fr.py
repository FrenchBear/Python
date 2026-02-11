# fr.py
# Play with fractions
#
# 2026-02-11    PV

"""
I'd like a Python program working on fractions.
First, given MAX varying from 1 to 100, find the set f of all simplified, distinct fractions n/d with 0<n<d<=MAX.
Then I'd like a simple plot of the number of fractions in F in function of MAX.
Then, for a specific value of MAX=1000, compute the set f, and plot the histogram of values in say 50 buckets from 0 to 1.
"""

import math
import matplotlib.pyplot as plt


def get_fraction_count_series(limit: int) -> list[int]:
    """Returns a list of counts of simplified fractions for MAX varying from 1 to limit."""
    counts = []
    total_fractions = 0
    
    for d in range(1, limit + 1):
        # Calculate Euler's totient function phi(d) for n < d
        # We want 0 < n < d, so for d=1 there are no such n.
        phi = 0
        for n in range(1, d):
            if math.gcd(n, d) == 1:
                phi += 1
        
        total_fractions += phi
        counts.append(total_fractions)
        
    return counts


def get_fractions_values(max_d: int) -> list[float]:
    """Returns a list of float values of all simplified fractions with denominator <= max_d."""
    values = []
    for d in range(2, max_d + 1):
        for n in range(1, d):
            if math.gcd(n, d) == 1:
                values.append(n / d)
    return values


def main():
    # Part 1: Plot count vs MAX for MAX in 1..100
    max_limit_plot = 100
    counts = get_fraction_count_series(max_limit_plot)
    x_axis = list(range(1, max_limit_plot + 1))
    
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.plot(x_axis, counts, marker='.', markersize=2)
    plt.title(f"Count of simplified fractions |F| vs MAX (up to {max_limit_plot})")
    plt.xlabel("MAX")
    plt.ylabel("Number of Fractions")
    plt.grid(True)

    # Part 2: Histogram for MAX=1000
    max_d_hist = 1000
    print(f"Computing set F for MAX={max_d_hist}...")
    fraction_values = get_fractions_values(max_d_hist)
    print(f"Computed {len(fraction_values)} fractions.")

    plt.subplot(1, 2, 2)
    plt.hist(fraction_values, bins=50, edgecolor='black', linewidth=0.5)
    plt.title(f"Histogram of fraction values (MAX={max_d_hist})")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.grid(True, alpha=0.5)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
