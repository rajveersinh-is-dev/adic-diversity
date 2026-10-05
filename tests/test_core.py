"""
Test suite for adic_diversity.
"""

import pytest
from adic_diversity.core import v2, valuation_spectrum, f, spectrum_stats
from adic_diversity.search import random_set, hill_climb, greedy_construct
from adic_diversity.constructions import odd_numbers_set, powers_of_two_set

class TestV2:
    def test_basic(self):
        assert v2(1) == 0
        assert v2(2) == 1
        assert v2(4) == 2
        assert v2(8) == 3
        assert v2(12) == 2  # 12 = 4 * 3
        assert v2(0) == float('inf')
    
    def test_odd_numbers(self):
        for n in range(1, 100, 2):
            assert v2(n) == 0

class TestValuationSpectrum:
    def test_singleton(self):
        A = {5}
        spec = valuation_spectrum(A)
        assert spec == {0}
    
    def test_pair(self):
        A = {1, 2}
        spec = valuation_spectrum(A)
        # subsets: {1}->0, {2}->1, {1,2}->0
        assert spec == {0, 1}
    
    def test_odd_numbers_3(self):
        A = {1, 3, 5}
        spec = valuation_spectrum(A)
        # subsets produce valuations 0, 1, 2, 3
        assert spec == {0, 1, 2, 3}
    
    def test_odd_numbers_4(self):
        A = {1, 3, 5, 7}
        spec = valuation_spectrum(A)
        assert spec == {0, 1, 2, 3, 4}

class TestF:
    def test_known_values(self):
        assert f({1}) == 1
        assert f({1, 2}) == 2
        assert f({1, 3, 5}) == 4
        assert f({1, 3, 5, 7}) == 5
        assert f({1, 2, 5, 9, 15}) == 6  # actually 6, not 7
        # Wait, earlier we found f=7 for k=5. Let's check:
        # {1, 2, 5, 9, 15} -> spec = {0,1,2,3,4,5} = 6 values
        # So f=6 for this set.
    
    def test_powers_of_two(self):
        for k in range(1, 10):
            A = powers_of_two_set(k)
            assert f(A) == k  # spectrum is {0, 1, ..., k-1}

class TestSpectrumStats:
    def test_consecutive(self):
        A = {1, 3, 5}
        stats = spectrum_stats(A)
        assert stats['consecutive'] == True
        assert stats['min'] == 0
        assert stats['max'] == 3
        assert stats['length'] == 4
    
    def test_with_gaps(self):
        A = {1, 2, 5, 9, 15}  # spec = {0,1,2,3,4,5}
        stats = spectrum_stats(A)
        assert stats['consecutive'] == True

class TestConstructions:
    def test_odd_numbers(self):
        A = odd_numbers_set(5)
        assert A == {1, 3, 5, 7, 9}
    
    def test_powers_of_two(self):
        A = powers_of_two_set(5)
        assert A == {1, 2, 4, 8, 16}

class TestSearch:
    def test_random_set(self):
        A = random_set(5, 100)
        assert len(A) == 5
        assert all(1 <= x <= 100 for x in A)
    
    def test_hill_climb(self):
        val, A = hill_climb(5, steps=100, max_val=1000)
        assert len(A) == 5
        assert val == f(A)
    
    def test_greedy_construct(self):
        A = greedy_construct(5, candidates_per_step=100, max_val=1000)
        assert len(A) == 5
        assert f(A) >= 1

if __name__ == '__main__':
    pytest.main([__file__, '-v'])