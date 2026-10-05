#!/usr/bin/env python3
"""Generate figures for the paper."""

import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Load results
with open('results/extensive.json') as f:
    data = json.load(f)

ks = [d['k'] for d in data]
fs = [d['max_f'] for d in data]
consecutive = [d['consecutive'] for d in data]
spans = [d['span'] for d in data]

# Full range for reference lines
all_ks = list(range(1, 17))
# Extend fs for full range (fill in known values for k=1..4)
full_fs = [1, 2, 4, 5] + fs

# Figure 1: f(k) vs k
plt.figure(figsize=(8, 5))
plt.plot(all_ks, full_fs, 'bo-', label='Best found $f(k)$')
plt.plot(all_ks, all_ks, 'r--', label='$f(k)=k$ (powers of 2)')
plt.plot(all_ks, [k//2 + 2 for k in all_ks], 'g--', label='$f(k) \\approx k/2$ (odd numbers)')
plt.plot(all_ks, [1.5*k for k in all_ks], 'k:', label='$1.5k$')
plt.xlabel('$k$ (set size)')
plt.ylabel('$f(k)$ (max distinct valuations)')
plt.title('Maximum 2-adic Valuation Diversity of Subset Sums')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('figures/fk_vs_k.png', dpi=200)
plt.close()

# Figure 2: Ratio f(k)/k
plt.figure(figsize=(8, 5))
full_ratios = [f/k for f, k in zip(full_fs, all_ks)]
plt.plot(all_ks, full_ratios, 'bo-')
plt.axhline(y=1.5, color='k', linestyle=':', label='1.5')
plt.xlabel('$k$')
plt.ylabel('$f(k)/k$')
plt.title('Ratio of Maximum Valuation Diversity to Set Size')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('figures/ratio.png', dpi=200)
plt.close()

# Figure 3: Spectrum visualization for k=8 (consecutive)
from adic_diversity import valuation_spectrum
# Use the k=8 example from results
k8_example = set(data[7]['example'])  # k=8 is index 7
spec = sorted(valuation_spectrum(k8_example))

plt.figure(figsize=(10, 3))
colors = ['green' if v in spec else 'red' for v in range(max(spec)+1)]
plt.bar(range(max(spec)+1), [1]* (max(spec)+1), color=colors, edgecolor='black')
plt.xlabel('2-adic valuation $\\nu_2$')
plt.ylabel('Present')
plt.title(f'Valuation Spectrum for k=8 (consecutive $[0,{max(spec)}]$)')
plt.tight_layout()
plt.savefig('figures/spectrum_k8.png', dpi=200)
plt.close()

# Figure 4: Spectrum for k=10 (with gaps)
k10_example = set(data[9]['example'])
spec = sorted(valuation_spectrum(k10_example))
gaps = [v for v in range(max(spec)+1) if v not in spec]

plt.figure(figsize=(10, 3))
colors = ['green' if v in spec else 'red' for v in range(max(spec)+1)]
plt.bar(range(max(spec)+1), [1]* (max(spec)+1), color=colors, edgecolor='black')
plt.xlabel('2-adic valuation $\\nu_2$')
plt.ylabel('Present')
plt.title(f'Valuation Spectrum for k=10 (gaps at {gaps})')
plt.tight_layout()
plt.savefig('figures/spectrum_k10.png', dpi=200)
plt.close()

# Figure 5: Comparison of constructions
from adic_diversity import f, odd_numbers_set, powers_of_two_set
k_vals = all_ks
powers_f = [f(powers_of_two_set(k)) for k in k_vals]
odd_f = [f(odd_numbers_set(k)) for k in k_vals]

plt.figure(figsize=(8, 5))
plt.plot(k_vals, full_fs, 'bo-', label='Best found (search)')
plt.plot(k_vals, powers_f, 'r--', label='Powers of 2 ($f=k$)')
plt.plot(k_vals, odd_f, 'g--', label='Odd numbers ($f \\approx k/2$)')
plt.xlabel('$k$')
plt.ylabel('$f(k)$')
plt.title('Comparison of Constructions')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('figures/constructions_comparison.png', dpi=200)
plt.close()

print("Figures saved to figures/")