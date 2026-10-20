import glob
import math
import os

import pytest

import pycatch22 as catch22

# pycatch22 must reproduce the catch22 C exactly: compare with the expected outputs
# committed in catch22's testData (in the catch22 submodule), which run_features
# writes as lines of "value, feature name, computation time (ms)" (catch24, masked)
TEST_DATA = os.path.join(os.path.dirname(__file__), '..', 'src', 'catch22', 'testData')


def load_series(path):
    # values separated by any whitespace (one per line, or several on a line)
    with open(path) as f:
        return [float(v) for v in f.read().split()]


def load_expected(path):
    expected = {}
    with open(path) as f:
        for line in f:
            parts = [p.strip() for p in line.split(',')]
            if len(parts) >= 2 and parts[1]:
                expected[parts[1]] = float(parts[0])
    return expected


def find_cases():
    cases = []
    for out_path in sorted(glob.glob(os.path.join(TEST_DATA, '*', '*_output.txt'))):
        in_path = out_path.replace('_output.txt', '.txt')
        if os.path.exists(in_path):
            cases.append(pytest.param(in_path, out_path, id=os.path.basename(in_path)))
    return cases


CASES = find_cases()


@pytest.mark.filterwarnings("ignore:the time series is empty or contains NaN/Inf")
@pytest.mark.skipif(not CASES, reason="catch22 submodule not checked out")
@pytest.mark.parametrize("in_path, out_path", CASES)
def test_matches_catch22_c(in_path, out_path):
    expected = load_expected(out_path)
    res = catch22.catch22_all(load_series(in_path), catch24=True)
    assert len(expected) == 24, f"Expected 24 features in {out_path}."
    for name, value in zip(res['names'], res['values']):
        exp = expected[name]
        if math.isnan(exp):
            assert math.isnan(value), f"{name}: expected NaN, got {value}."
        else:
            # the expected outputs are printed to 14 decimal places
            assert abs(value - exp) <= 1e-9 * max(1.0, abs(exp)), f"{name}: got {value}, expected {exp}."
