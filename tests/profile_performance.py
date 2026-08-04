"""Profile pycatch22 runtime as a function of time-series length.

Runs catch22 over synthetic time series with lengths spanning several orders of magnitude
and reports the mean wall-clock time per length. Intended as a lightweight
performance smoke-test for CI.
"""
import argparse
import glob
import os
import time

import numpy as np

import pycatch22 as catch22

EMPIRICAL_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "src", "catch22", "testData", "empirical",
)


def profile(lengths, repeats, catch24=True, seed=0):
    """Return a list of (length, mean_seconds, std_seconds) tuples."""
    rng = np.random.default_rng(seed)
    results = []
    for n in lengths:
        data = rng.standard_normal(n).tolist()
        timings = []
        for _ in range(repeats):
            start = time.perf_counter()
            catch22.catch22_all(data, catch24=catch24)
            timings.append(time.perf_counter() - start)
        timings = np.asarray(timings)
        results.append((n, float(timings.mean()), float(timings.std())))
    return results

def run_empirical_test(catch24=True, data_dir=EMPIRICAL_DIR, repeats=0):
    """Run catch22_all on every empirical time series and report the total time.

    Loads each time-series file in ``data_dir`` (excluding the ``_output`` files),
    runs ``catch22_all`` on it, and returns the total wall-clock seconds taken to
    process all files along with the number of files processed.
    """
    files = sorted(
        f for f in glob.glob(os.path.join(data_dir, "*.txt"))
        if not f.endswith("_output.txt")
    )

    per_repeat_time = []
    for _ in range(max(repeats, 1)):
        total = 0.0
        for path in files:
            data = np.loadtxt(path).tolist()
            start = time.perf_counter()
            catch22.catch22_all(data, catch24=catch24)
            total += time.perf_counter() - start
        per_repeat_time.append(total)

    return np.mean(per_repeat_time), np.std(per_repeat_time)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min-exp", type=int, default=0,
                        help="minimum length exponent (base 10)")
    parser.add_argument("--max-exp", type=int, default=5,
                        help="maximum length exponent (base 10)")
    parser.add_argument("--repeats", type=int, default=3,
                        help="number of repeats per length")
    parser.add_argument("--catch24", action="store_true",
                        help="profile catch24 (includes mean and std)")
    args = parser.parse_args()

    lengths = [10 ** e for e in range(args.min_exp, args.max_exp + 1)]
    results = profile(lengths, args.repeats, catch24=args.catch24)

    print(f"{'length':>10} {'mean (s)':>14} {'std (s)':>14}")
    for n, mean, std in results:
        print(f"{n:>10} {mean:>14.6f} {std:>14.6f}")
    
    mean_e1000, std_e1000 = run_empirical_test(repeats=3)
    print(f'Total time taken to run on Empirical1000: {mean_e1000:>.6f} +/- {std_e1000:>.6f} s')


if __name__ == "__main__":
    main()
