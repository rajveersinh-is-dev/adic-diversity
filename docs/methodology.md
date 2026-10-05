# Methodology

This document describes the research methodology used in this project.

## Problem Discovery

The problem was discovered through systematic exploration of p-adic valuation properties of subset sums. 
Initial searches focused on:
1. Known literature on distinct subset sums (Erdős problem)
2. p-adic analysis of sumsets
3. Binary carry propagation in addition

The specific question — "maximize the number of distinct 2-adic valuations of subset sums" — did not appear in:
- OEIS (checked sequences 1,2,4,5,7,9,11,12,14,16,17,19,20,21,22,23)
- arXiv (searched for "2-adic valuation subset sums", "p-adic valuation subset sums")
- Google Scholar (searched related terms)

## Computational Approach

### Core Functions
- `v2(n)`: 2-adic valuation via bit operations
- `valuation_spectrum(A)`: computes all valuations of subset sums
- `f(A)`: returns cardinality of spectrum

### Search Algorithms

1. **Greedy Construction** (`greedy_construct`)
   - Start with empty set
   - At each step, try `candidates_per_step` random integers
   - Add the one maximizing `f(A ∪ {x})`
   - Fast, finds good local optima

2. **Hill Climbing** (`hill_climb`)
   - Start from random set
   - Mutate one element at a time (bit flips, power-of-2 additions, etc.)
   - Accept if `f` does not decrease
   - Escapes shallow local optima

3. **Simulated Annealing** (`simulated_annealing`)
   - Similar to hill climbing but accepts decreases with probability `exp(Δ/T)`
   - Temperature decays from `temp_start` to `temp_end`
   - Better global exploration

4. **Multi-start** (`multi_start_search`)
   - Runs any search method multiple times with different random seeds
   - Returns best result across restarts

### Experimental Protocol

1. For each k=1..16:
   - Run multi-start greedy (30 restarts, 2000 candidates/step)
   - Run multi-start hill climbing (30 restarts, 500 steps)
   - Run multi-start annealing (10 restarts, 2000 iterations)
   - Keep best across all methods
   - Record: f(A), spectrum, consecutiveness, example set

2. Save results to JSON and CSV for reproducibility

3. Verify results by recomputing f(A) from saved examples

## Validation

### Internal Consistency
- All reported f(A) values verified by recomputation
- Spectra confirmed to match reported sets
- Search methods cross-validated (different methods found same optima for k≤10)

### Edge Cases Tested
- k=1,2: trivial cases
- Sets with all odd elements
- Sets with powers of two
- Large numbers (up to 10^9) to rule out small-number artifacts

### Negative Results
- Exhaustive search for k≤4, max_val≤12 confirmed optimality for small cases
- No set found with f(k) > floor(1.5k) + 1 for k≤16
- Consecutive spectra only for specific k values

## Limitations

1. **Heuristic search only**: For k>10, we cannot guarantee global optimality
2. **No formal proof of upper bounds**: Conjectured bounds based on empirical evidence
3. **Limited to k≤16**: Computational cost grows exponentially (2^k subset sums)
4. **Single prime (2)**: Generalization to odd primes not explored
5. **No uniqueness analysis**: Optimal sets may not be unique

## Reproducibility

All experiments can be reproduced by running:
```bash
python experiments/run_systematic.py
python experiments/run_extensive.py
```

Results are deterministic given the random seeds used in the scripts.