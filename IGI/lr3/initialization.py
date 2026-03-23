"""
Purpose: Sequence initialization functions (via input and generator)
Lab: Laboratory Work 3
Version: 1.0
Developer: Kushniarou A D
Date: 2026-03-23
"""

import random

def init_via_input(seq: list, size: int) -> None:
    """
    Initializes the provided sequence via user input.
    """
    seq.clear()
    print(f"Please enter {size} float numbers:")
    for i in range(size):
        while True:
            try:
                val = float(input(f"Element {i+1}: "))
                seq.append(val)
                break
            except ValueError:
                print("Invalid input. Please enter a valid float number.")

def _generator_func(size: int, min_val: float = -20.0, max_val: float = 20.0):
    """
    A true generator function yielding random float values.
    """
    for _ in range(size):
        yield round(random.uniform(min_val, max_val), 2)

def init_via_generator(seq: list, size: int) -> None:
    """
    Initializes the provided sequence using the generator function.
    """
    seq.clear()
    for val in _generator_func(size):
        seq.append(val)


