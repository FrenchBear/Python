# Empirical comparison between population standard deviation and sample standard deviation
#
# DM-32 manual:
# - Population standard deviation assumes the data being analyzed is the complete set.
# - Sample standard deviation assumes the data being analyzed is a sample of a larger set. It uses a slightly different
#   formula because it would otherwise give a consistently underestimated variability. By making the deviation value
#   artificially larger, sample standard deviation, while not unbiased, gives a more accurate inference for the partial set.
#
# 2025-12-22    PV

import random
import math

def get_random_list(n: int, distrib: int) -> list[float]:
    """
    Returns a list of n random data (float values), using a varying distribution model:
    - if distrib=1 then use a uniform random distribution of values between 0 and 20
    - if distrib=2 then use a normal distribution of values with a mean of 10 and a standard deviation of 4
    - if distrib=3 then use an exponential distribution function with parameter lambda=0.5
    """
    match distrib:
        case 1:
            return [random.uniform(0, 20) for _ in range(n)]
        case 2:
            return [random.normalvariate(10, 4) for _ in range(n)]
        case 3:
            return [random.expovariate(0.5) for _ in range(n)]
    return []

def variance(l: list[float], pop: bool = True) -> float:
    """
    Computes the variance of values of l.
    - if pop is True (default), computes population variance (denominator n)
    - if pop is False, computes sample variance (denominator n-1)
    """
    n = len(l)
    if n < 2:
        return 0.0
    mean = sum(l) / n
    variance = sum((x - mean) ** 2 for x in l)
    if pop:
        variance /= n
    else:
        variance /= (n - 1)
    return variance

def standard_deviation(l: list[float], pop: bool = True) -> float:
    """
    Computes the standard deviation of values of l.
    - if pop is True (default), computes population standard deviation (denominator n)
    - if pop is False, computes sample standard deviation (denominator n-1)
    """
    return math.sqrt(variance(l, pop))

def run_test(pop_count: int, sample_count: int, distrib: int, loops: int):
    pop = get_random_list(pop_count, distrib)
    base_var = variance(pop)
    print(f"Using a list of {pop_count} random values, {['uniform','normal','exponential'][distrib]} distribution, taking samples of {sample_count} values")
    print(f"Full list variance: {base_var:.3f}\n")
    print("        pop     sam  ")
    print("       ------  ------")
    pop_best = 0
    sam_best = 0
    for loop in range(loops):
        sample = random.sample(pop, sample_count)
        pop_var = variance(sample)
        sam_var = variance(sample, False)
        best = 'pop' if abs(pop_var-base_var)<abs(sam_var-base_var) else 'sam'
        print(f"[{loop + 1:0>2}]:  {pop_var:6.3f}  {sam_var:6.3f}  {best}")
        if best=='pop':
            pop_best+=1
        else:
            sam_best+=1
    print()
    print(f"Population variance better: {pop_best/loops:4.1%}")
    print(f"Sample variance better:     {sam_best/loops:4.1%}")


run_test(100, 20, 1, 10)
