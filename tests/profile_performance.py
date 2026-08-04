"""Profile pycatch22 runtime as a function of time-series length.

Runs catch22 over synthetic time series with lengths spanning 10^0 to 10^6
and reports the mean wall-clock time per length. Intended as a lightweight
performance smoke-test for CI.
"""
import argparse
import time

import numpy as np

import pycatch22 as catch22


def profile(lengths, repeats, catch24=False, seed=0):
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min-exp", type=int, default=0,
                        help="minimum length exponent (base 10)")
    parser.add_argument("--max-exp", type=int, default=6,
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


if __name__ == "__main__":
    main()
