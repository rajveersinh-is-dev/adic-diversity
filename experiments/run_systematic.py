#!/usr/bin/env python3
"""
Run systematic experiments to find maximum f(k) for small k.
"""

import json
from pathlib import Path
from adic_diversity.experiments import exhaustive_search, benchmark_constructions, systematic_greedy, save_results

def main():
    print("Running systematic experiments...")
    
    # Exhaustive search for small k (only very small) - SKIP for now
    print("\n1. Exhaustive search - SKIPPED (too slow)")
    exhaustive_results = []
    # for k in range(1, 5):
    #     for max_val in range(k + 2, min(13, k + 8)):
    #         print(f"  k={k}, max_val={max_val}...")
    #         res = exhaustive_search(k, max_val)
    #         exhaustive_results.append(res)
    #         print(f"    max_f={res['max_f']}, num_optimal={res['num_optimal']}")
    
    # save_results(exhaustive_results, 'results/exhaustive')
    # print("  Saved to results/exhaustive.json")
    
    # Benchmark standard constructions
    print("\n2. Benchmark constructions")
    bench_results = benchmark_constructions(16)
    save_results(bench_results, 'results/constructions')
    print("  Saved to results/constructions.json")
    
    # Systematic greedy search (reduced trials)
    print("\n3. Systematic greedy search (10 trials each)")
    greedy_results = systematic_greedy(12, trials=10, max_val=50000)
    save_results(greedy_results, 'results/greedy')
    print("  Saved to results/greedy.json")
    
    # Print summary table
    print("\n=== Summary of Best Known f(k) ===")
    print("k  :  greedy  |  odd  |  pow2")
    print("-------------------------------")
    for r in greedy_results:
        k = r['k']
        bench = next(b for b in bench_results if b['k'] == k)
        print(f"{k:2d} :  {r['max_f']:2d}      |  {bench['odd_f']:2d}  |  {bench['powers2_f']:2d}")

if __name__ == '__main__':
    main()