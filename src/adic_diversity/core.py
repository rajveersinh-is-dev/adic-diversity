"""
Core functions for 2-adic valuation diversity of subset sums.
"""

from itertools import combinations
from typing import Set, FrozenSet, Iterable

def v2(n: int) -> int:
    """2-adic valuation: exponent of highest power of 2 dividing n.
    v2(0) = float('inf') (not used for nonempty subsets of positive integers)."""
    if n == 0:
        return float('inf')
    c = 0
    while n % 2 == 0:
        n //= 2
        c += 1
    return c

def valuation_spectrum(A: Set[int]) -> Set[int]:
    """Return the set of 2-adic valuations of all nonempty subset sums of A."""
    A_list = list(A)
    return {v2(sum(S)) for r in range(1, len(A_list) + 1) for S in combinations(A_list, r)}

def f(A: Set[int]) -> int:
    """Number of distinct 2-adic valuations of nonempty subset sums of A."""
    return len(valuation_spectrum(A))

def is_optimal(A: Set[int], known_max: int) -> bool:
    """Check if A achieves the known maximum for its size."""
    return f(A) == known_max

def spectrum_stats(A: Set[int]) -> dict:
    """Return statistics about the valuation spectrum of A."""
    spec = valuation_spectrum(A)
    if not spec:
        return {'min': None, 'max': None, 'consecutive': False, 'length': 0, 'gaps': []}
    spec_list = sorted(spec)
    mn, mx = spec_list[0], spec_list[-1]
    consecutive = (mx - mn + 1 == len(spec))
    gaps = [v for v in range(mn, mx + 1) if v not in spec]
    return {
        'min': mn,
        'max': mx,
        'consecutive': consecutive,
        'length': len(spec),
        'span': mx - mn + 1,
        'gaps': gaps,
        'spectrum': spec_list
    }