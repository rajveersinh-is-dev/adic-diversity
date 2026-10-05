"""
Search algorithms for maximizing 2-adic valuation diversity.
"""

import random
from typing import Set, List, Tuple, Optional, Callable
from .core import f, valuation_spectrum

def random_set(k: int, max_val: int = 10**9) -> Set[int]:
    """Generate random k-element set."""
    return set(random.sample(range(1, max_val + 1), k))

def random_search(k: int, trials: int = 10000, max_val: int = 10**9) -> Tuple[int, Set[int]]:
    """Pure random search for maximum f."""
    best_val = 0
    best_set = None
    for _ in range(trials):
        A = random_set(k, max_val)
        val = f(A)
        if val > best_val:
            best_val = val
            best_set = A
    return best_val, best_set

def mutate(A: Set[int], max_val: int = 10**9) -> Set[int]:
    """Mutate a set by changing one element."""
    A_list = list(A)
    i = random.randrange(len(A_list))
    B = A_list.copy()
    op = random.choice(['bitflip', 'add_pow2', 'add_sub', 'xor', 'replace'])
    if op == 'bitflip':
        bit = random.randrange(30)
        B[i] ^= (1 << bit)
    elif op == 'add_pow2':
        pow2 = 1 << random.randrange(20)
        B[i] = max(1, B[i] + random.choice([-pow2, pow2]))
    elif op == 'add_sub':
        B[i] = max(1, B[i] + random.randint(-100, 100))
    elif op == 'xor':
        B[i] ^= random.randint(1, 2**20 - 1)
    elif op == 'replace':
        B[i] = random.randint(1, max_val)
    if len(set(B)) == len(B) and all(b > 0 for b in B):
        return set(B)
    return A

def hill_climb(k: int, steps: int = 1000, max_val: int = 10**9,
               start_set: Optional[Set[int]] = None) -> Tuple[int, Set[int]]:
    """Hill climbing search."""
    A = start_set if start_set else random_set(k, max_val)
    best_val = f(A)
    best_A = set(A)
    for _ in range(steps):
        B = mutate(A, max_val)
        val = f(B)
        if val >= f(A):
            A = B
        if val > best_val:
            best_val = val
            best_A = set(B)
    return best_val, best_A

def greedy_construct(k: int, candidates_per_step: int = 5000,
                     max_val: int = 10**6) -> Set[int]:
    """Greedy construction: add elements one by one to maximize f."""
    A = set()
    for step in range(k):
        best_val = -1
        best_x = None
        for _ in range(candidates_per_step):
            x = random.randint(1, max_val)
            if x in A:
                continue
            val = f(A | {x})
            if val > best_val:
                best_val = val
                best_x = x
        if best_x is not None:
            A.add(best_x)
        else:
            break
    return A

def simulated_annealing(k: int, iterations: int = 10000,
                        max_val: int = 10**9,
                        temp_start: float = 1.0,
                        temp_end: float = 0.01) -> Tuple[int, Set[int]]:
    """Simulated annealing search."""
    A = random_set(k, max_val)
    best_val = f(A)
    best_A = set(A)
    current_val = best_val
    current_A = set(A)
    
    for i in range(iterations):
        temp = temp_start * (temp_end / temp_start) ** (i / iterations)
        B = mutate(current_A, max_val)
        val = f(B)
        delta = val - current_val
        if delta > 0 or random.random() < pow(2.718, delta / temp):
            current_A = B
            current_val = val
            if val > best_val:
                best_val = val
                best_A = set(B)
    return best_val, best_A

def multi_start_search(k: int, restarts: int = 20,
                       method: str = 'hill_climb',
                       **kwargs) -> Tuple[int, Set[int]]:
    """Run multiple restarts of a search method."""
    methods = {
        'hill_climb': hill_climb,
        'greedy': greedy_construct,
        'annealing': simulated_annealing,
    }
    search_fn = methods[method]
    best_val = 0
    best_A = None
    for r in range(restarts):
        val, A = search_fn(k, **kwargs)
        if val > best_val:
            best_val = val
            best_A = A
    return best_val, best_A