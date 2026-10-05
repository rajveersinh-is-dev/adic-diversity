#!/usr/bin/env python3
"""Generate figures for the *adic-diversity* paper.

The script reads the JSON file ``results/extensive.json`` produced by the
experiment suite and creates a series of PNG figures in the ``figures``
directory.  It is deliberately lightweight – the heavy lifting (valuation
spectrum, construction helpers, etc.) lives in the :pymod:`adic_diversity`
package.

The implementation has been modernised for Python 3.10+:

*   Redundant imports (``numpy``) have been removed.
*   All public functions are type‑annotated and documented.
*   Errors such as a missing ``results`` file are reported with a clear
    ``FileNotFoundError`` instead of an obscure ``IOError``.
*   The ``figures`` output directory is created automatically.
*   The script is now structured around a ``main()`` function, making the
    module import‑safe while preserving the original command‑line behaviour.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import List, Sequence

import matplotlib
import matplotlib.pyplot as plt

# ``matplotlib`` must use a non‑interactive backend when the script is run in
# headless environments (e.g., CI).  The original code set this globally; we
# keep the behaviour but do it as early as possible.
matplotlib.use("Agg")

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def load_results(path: Path) -> List[dict]:
    """Load the experiment results from *path*.

    Parameters
    ----------
    path:
        Path to the JSON file containing a list of result dictionaries.

    Returns
    -------
    list[dict]
        The parsed JSON data.

    Raises
    ------
    FileNotFoundError
        If *path* does not exist.
    json.JSONDecodeError
        If the file cannot be parsed as JSON.
    """
    if not path.is_file():
        raise FileNotFoundError(f"Results file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def ensure_dir(path: Path) -> None:
    """Create *path* (and parents) if it does not already exist.

    The function is a thin wrapper around :pymeth:`Path.mkdir` that swallows the
    ``FileExistsError`` when the directory is already present.
    """
    path.mkdir(parents=True, exist_ok=True)


def plot_f_vs_k(all_ks: Sequence[int], full_fs: Sequence[int], out_path: Path) -> None:
    """Plot ``f(k)`` against ``k`` and save the figure.

    Parameters
    ----------
    all_ks:
        The full range of ``k`` values (e.g., ``1..16``).
    full_fs:
        Corresponding ``f(k)`` values, padded with the known base cases.
    out_path:
        Destination file for the PNG image.
    """
    plt.figure(figsize=(8, 5))
    plt.plot(all_ks, full_fs, "bo-", label="Best found $f(k)$")
    plt.plot(all_ks, list(all_ks), "r--", label="$f(k)=k$ (powers of 2)")
    plt.plot(all_ks, [k // 2 + 2 for k in all_ks], "g--", label="$f(k) \approx k/2$ (odd numbers)")
    plt.plot(all_ks, [1.5 * k for k in all_ks], "k:", label="$1.5k$")
    plt.xlabel("$k$ (set size)")
    plt.ylabel("$f(k)$ (max distinct valuations)")
    plt.title("Maximum 2-adic Valuation Diversity of Subset Sums")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def plot_ratio(all_ks: Sequence[int], full_fs: Sequence[int], out_path: Path) -> None:
    """Plot the ratio ``f(k)/k`` and save the figure.

    Parameters are analogous to :func:`plot_f_vs_k`.
    """
    ratios = [f / k for f, k in zip(full_fs, all_ks)]
    plt.figure(figsize=(8, 5))
    plt.plot(all_ks, ratios, "bo-")
    plt.axhline(y=1.5, color="k", linestyle=":", label="1.5")
    plt.xlabel("$k$")
    plt.ylabel("$f(k)/k$")
    plt.title("Ratio of Maximum Valuation Diversity to Set Size")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def plot_spectrum(k: int, example_set: set[int], out_path: Path, *, title_suffix: str) -> None:
    """Create a bar‑plot visualising the 2‑adic valuation spectrum.

    Parameters
    ----------
    k:
        The size of the set (used only for the title).
    example_set:
        The concrete set of integers whose spectrum is to be displayed.
    out_path:
        Destination PNG file.
    title_suffix:
        Additional description appended to the plot title (e.g., "consecutive"
        or "gaps at …").
    """
    from adic_diversity import valuation_spectrum

    spec = sorted(valuation_spectrum(example_set))
    max_val = max(spec)
    colors = ["green" if v in spec else "red" for v in range(max_val + 1)]
    plt.figure(figsize=(10, 3))
    plt.bar(range(max_val + 1), [1] * (max_val + 1), color=colors, edgecolor="black")
    plt.xlabel("2-adic valuation $\\nu_2$")
    plt.ylabel("Present")
    plt.title(f"Valuation Spectrum for k={k} ({title_suffix})")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def plot_constructions(all_ks: Sequence[int], full_fs: Sequence[int], out_path: Path) -> None:
    """Compare the best‑found construction with two simple families.

    The families are provided by :func:`adic_diversity.powers_of_two_set` and
    :func:`adic_diversity.odd_numbers_set`.
    """
    from adic_diversity import f, odd_numbers_set, powers_of_two_set

    powers_f = [f(powers_of_two_set(k)) for k in all_ks]
    odd_f = [f(odd_numbers_set(k)) for k in all_ks]

    plt.figure(figsize=(8, 5))
    plt.plot(all_ks, full_fs, "bo-", label="Best found (search)")
    plt.plot(all_ks, powers_f, "r--", label="Powers of 2 ($f=k$)")
    plt.plot(all_ks, odd_f, "g--", label="Odd numbers ($f \approx k/2$)")
    plt.xlabel("$k$")
    plt.ylabel("$f(k)$")
    plt.title("Comparison of Constructions")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def main() -> None:
    """Entry point for the script.

    The function orchestrates loading the data, preparing the derived lists,
    ensuring the output directory exists, and delegating to the individual
    plotting helpers.
    """
    results_path = Path("results/extensive.json")
    try:
        data = load_results(results_path)
    except FileNotFoundError as exc:
        sys.stderr.write(str(exc) + "\n")
        sys.exit(1)

    # Extract columns – the JSON schema is guaranteed by the experiment code.
    ks: List[int] = [int(d["k"]) for d in data]
    fs: List[int] = [int(d["max_f"]) for d in data]
    # ``consecutive`` and ``span`` are not used directly in the plots but are
    # retained for potential future extensions.
    _ = [d["consecutive"] for d in data]
    _ = [d["span"] for d in data]

    # Full range for reference lines (the paper uses k=1..16).
    all_ks = list(range(1, 17))
    # Pad the experimentally discovered ``fs`` with the known base cases for
    # k=1..4.  The original script assumed the order matches ``all_ks`` after the
    # first four entries.
    full_fs = [1, 2, 4, 5] + fs

    figures_dir = Path("figures")
    ensure_dir(figures_dir)

    # 1️⃣ f(k) vs k
    plot_f_vs_k(all_ks, full_fs, figures_dir / "fk_vs_k.png")

    # 2️⃣ Ratio f(k)/k
    plot_ratio(all_ks, full_fs, figures_dir / "ratio.png")

    # 3️⃣ Spectrum for k=8 (consecutive)
    k8_example = set(data[7]["example"])  # index 7 corresponds to k=8
    plot_spectrum(
        k=8,
        example_set=k8_example,
        out_path=figures_dir / "spectrum_k8.png",
        title_suffix=f"consecutive $[0,{max(sorted(k8_example))}]$",
    )

    # 4️⃣ Spectrum for k=10 (with gaps)
    k10_example = set(data[9]["example"])  # index 9 corresponds to k=10
    spec10 = sorted(k10_example)  # used only for title generation
    gaps = [v for v in range(max(spec10) + 1) if v not in spec10]
    plot_spectrum(
        k=10,
        example_set=k10_example,
        out_path=figures_dir / "spectrum_k10.png",
        title_suffix=f"gaps at {gaps}",
    )

    # 5️⃣ Comparison of constructions
    plot_constructions(all_ks, full_fs, figures_dir / "constructions_comparison.png")

    print("Figures saved to figures/")


if __name__ == "__main__":
    main()
