"""
adic_diversity: 2-adic valuation diversity of subset sums.

For a finite set A of integers, define f(A) as the number of distinct
2-adic valuations of all nonempty subset sums of A.

This package provides tools to compute f(A), search for maximal sets,
and explore the mathematical structure of the problem.
"""


__all__ = [
    'v2',
    'valuation_spectrum',
    'f',
    'greedy_construct',
    'random_search',
    'hill_climb',
    'consecutive_block_construction',
    'powers_of_two_set',
    'odd_numbers_set',
]

__version__ = '0.1.0'