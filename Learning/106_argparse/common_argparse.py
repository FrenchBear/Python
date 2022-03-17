# common_argparse.py
# Helpers functions for argparse
#
# 2022-03-17    PV

import argparse

def int_range(arg: str, low: int, high: int):
    def raise_err():
        raise argparse.ArgumentTypeError(f"Must be an integer beween {low} and {high}")

    try:
        n = int(arg)
    except ValueError:
        raise_err()
    if not low <= n <= high:
        raise_err()
    return n
