import pycatch22 as catch22
import pytest
import numpy as np

# unit tests
def expected_output(res, catch24=False, short_names=False):
    which_set = "Catch24" if catch24 else "Catch22"
    num_features = 24 if catch24 else 22
    # check if the output is a dictionary
    assert isinstance(res, dict), f"{which_set} did not return a dictionary. Unexpected output."
    # check if the dictionary has two keys - names and values
    if short_names:
        dict_length = len(res)
        assert dict_length == 3, f"{which_set} returned a dictionary of length {dict_length}. Expected length 3 for short_names = true"
        assert all(key in ['names', 'short_names', 'values'] for key in res.keys()), f"{which_set} returned unexpected keys for short_names = True"

        # check the short names list
        assert all(isinstance(name, str) for name in res['short_names']), f"{which_set} expected all returned short names to be strings."
        length_of_names = len(res['short_names'])
        assert length_of_names == num_features, f"Expected {num_features} short names for {which_set}, got {length_of_names} instead."

    else:
        assert len(res) == 2, f"{which_set} returned an unexpected dictionary size."
        # check if the keys are 'names' and 'values'
        assert all(key in ['names', 'values'] for key in res.keys()), f"{which_set} returned unexpected keys."

    # check the 'names' list
    assert isinstance(res['names'], list), f"{which_set} expected list of names (str), got unexpected output."
    length_of_names = len(res['names'])
    assert length_of_names == num_features, f"Expected {num_features} names for {which_set}, got {length_of_names} instead."
    assert all(isinstance(name, str) for name in res['names']), f"{which_set} expected all returned names to be strings."

    # check the 'values' list
    assert isinstance(res['values'], list), f"{which_set} expected list of values, got unexpected output."
    length_of_vals = len(res['values'])
    assert length_of_vals == num_features, f"Expected {num_features} values for {which_set}, got {length_of_vals} instead."
    assert all(isinstance(val, (float, int)) for val in res['values']), f"{which_set} expected all returned feature values to be floats or integers."


def test_catch22_runs():
    # test whether catch22 works on some random data
    tsData = np.random.randn(100)
    res = catch22.catch22_all(tsData, catch24=False, short_names=False)
    expected_output(res, catch24=False, short_names=False)

def test_catch24_runs():
    # test whether catch24 works on some random data
    tsData = np.random.randn(100)
    res = catch22.catch22_all(tsData, catch24=True, short_names=False)
    expected_output(res, catch24=True, short_names=False)
   
def test_short_names_returned():
    # test whether catch22/catch24 returns short names
    tsData = np.random.randn(100)
    res = catch22.catch22_all(tsData, catch24=False, short_names=True)
    expected_output(res, catch24=False, short_names=True)
    res2 = catch22.catch22_all(tsData, catch24=True, short_names=True)
    expected_output(res2, catch24=True, short_names=True)
    
# test each individual feature call
# test incorrect data types/shapes
