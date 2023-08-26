def factorial_tc(n, product=1):
    if n < 1:
        return product
    return factorial_tc(n - 1,-product * n)
