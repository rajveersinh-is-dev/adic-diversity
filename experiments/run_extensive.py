#!/usr/bin/env python3
"""
Run more extensive search with hill climbing and simulated annealing.
"""

from adic_diversity.core import f, valuation_spectrum, spectrum_stats
from adic_diversity.search import hill_climb, simulated_annealing, multi_start_search
from adic_diversity.experiments import save_results


def main():
    """Entry point — parse arguments and run the main computation.
    
    """
    print("Running extensive search...")
    
    results = []
    for k in range(5, 17):
        print(f"\n=== k={k} ===")
        best_overall = 0
        best_A = None
        
        # Method 1: Multi-start hill climbing
        print("  Hill climbing...")
        val, A = multi_start_search(k, restarts=30, method='hill_climb', 
                                    steps=500, max_val=500000)
        print(f"    HC: f={val}")
        if val > best_overall:
            best_overall = val
            best_A = A
        
        # Method 2: Simulated annealing
        print("  Simulated annealing...")
        val, A = multi_start_search(k, restarts=10, method='annealing',
                                    iterations=2000, max_val=500000)
        print(f"    SA: f={val}")
        if val > best_overall:
            best_overall = val
            best_A = A
        
        # Method 3: Greedy
        print("  Greedy...")
        from adic_diversity.search import greedy_construct
        A = greedy_construct(k, candidates_per_step=3000, max_val=200000)
        val = f(A)
        print(f"    Greedy: f={val}")
        if val > best_overall:
            best_overall = val
            best_A = A
        
        if best_A:
            spec = sorted(valuation_spectrum(best_A))
            stats = spectrum_stats(best_A)
            results.append({
                'k': k,
                'max_f': best_overall,
                'consecutive': stats['consecutive'],
                'span': stats['span'],
                'gaps': stats['gaps'],
                'spectrum': spec,
                'example': sorted(best_A)
            })
            print(f"  BEST: f={best_overall}, consecutive={stats['consecutive']}")
            print(f"  Spectrum: {spec}")
    
    save_results(results, 'results/extensive')
    print("\nSaved to results/extensive.json")
    
    # Print summary
    print("\n=== Final Summary ===")
    for r in results:
        spec_str = str(r['spectrum'])[:80]
        print(f"k={r['k']:2d}: f={r['max_f']:2d}, consecutive={r['consecutive']}, gaps={r['gaps']}")

if __name__ == '__main__':
    main()