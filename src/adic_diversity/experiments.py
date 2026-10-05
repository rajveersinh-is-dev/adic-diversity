"""
Systematic experiments for 2-adic valuation diversity.
"""

import json
import csv
from pathlib import Path
from typing import Dict, List, Tuple
from .core import f, valuation_spectrum, spectrum_stats
from .search import greedy_construct, random_search, hill_climb, multi_start_search
from .constructions import odd_numbers_set, powers_of_two_set

def exhaustive_search(k: int, max_val: int) -> Dict:
    """Exhaustive search for small k and max_val."""
    from itertools import combinations
    best_val = 0
    best_sets = []
    for A in combinations(range(1, max_val + 1), k):
        val = f(set(A))
        if val > best_val:
            best_val = val
            best_sets = [set(A)]
        elif val == best_val:
            best_sets.append(set(A))
    return {
        'k': k,
        'max_val': max_val,
        'max_f': best_val,
        'num_optimal': len(best_sets),
        'examples': [sorted(s) for s in best_sets[:10]]
    }

def benchmark_constructions(max_k: int = 12) -> List[Dict]:
    """Evaluate standard constructions."""
    results = []
    for k in range(1, max_k + 1):
        row = {'k': k}
        for name, fn in [('odd', odd_numbers_set), ('powers2', powers_of_two_set)]:
            A = fn(k)
            row[f'{name}_f'] = f(A)
            row[f'{name}_spec'] = str(sorted(valuation_spectrum(A)))
        results.append(row)
    return results

def systematic_greedy(max_k: int = 16, trials: int = 30, max_val: int = 100000) -> List[Dict]:
    """Run greedy search multiple times for each k."""
    results = []
    for k in range(1, max_k + 1):
        best = 0
        best_A = None
        for t in range(trials):
            A = greedy_construct(k, candidates_per_step=2000, max_val=max_val)
            val = f(A)
            if val > best:
                best = val
                best_A = A
        spec = sorted(valuation_spectrum(best_A)) if best_A else []
        stats = spectrum_stats(best_A) if best_A else {}
        results.append({
            'k': k,
            'max_f': best,
            'consecutive': stats.get('consecutive', False),
            'span': stats.get('span', 0),
            'gaps': stats.get('gaps', []),
            'example': sorted(best_A) if best_A else []
        })
    return results

def save_results(results: List[Dict], filepath: str):
    """Save results to JSON and CSV."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    # JSON
    with open(path.with_suffix('.json'), 'w') as jf:
        json.dump(results, jf, indent=2)
    
    # CSV
    if results:
        with open(path.with_suffix('.csv'), 'w', newline='') as cf:
            writer = csv.DictWriter(cf, fieldnames=results[0].keys())
            writer.writeheader()
            for row in results:
                # Convert lists to strings
                row_copy = {k: (str(v) if isinstance(v, list) else v) for k, v in row.items()}
                writer.writerow(row_copy)

def load_results(filepath: str) -> List[Dict]:
    """Load results from JSON."""
    with open(filepath, 'r') as f:
        return json.load(f)