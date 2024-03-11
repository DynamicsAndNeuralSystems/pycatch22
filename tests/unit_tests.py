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

def test_valid_input_types():
    # should accept tuples, arrays and lists
    data_as_tuple = (1, 2, 3, 4, 5, 6, 7, 8)
    res_tuple = catch22.catch22_all(data_as_tuple)
    expected_output(res_tuple)
    data_as_list = [1, 2, 3, 4, 5, 6, 7, 8]
    res_list = catch22.catch22_all(data_as_list)
    expected_output(res_list)
    data_as_numpy = np.array(data_as_list)
    res_numpy = catch22.catch22_all(data_as_numpy)
    expected_output(res_numpy)

def test_inf_and_nan_input():
    # pass in time series containing a NaN/inf, should return 0 (0.0) or NaN/inf outputs depending on feature
    zero_outputs = [2, 3, 9] # indexes of features with expected 0 or 0.0 output
    test_vals = [np.nan, np.inf, -np.inf]
    for val_type in test_vals:
        base_data = np.random.randn(100)
        base_data[0] = val_type
        res = catch22.catch22_all(base_data, catch24=False)
        expected_output(res, catch24=False, short_names=False)
        res_values = res['values']
        for i, val in enumerate(res_values):
            if i in zero_outputs:
                # check that value is 0 or 0.0
                assert val == 0 or val == 0.0, f"Expected 0 or 0.0 for feature {i+1} when passing ts containing {val_type}, got {val} instead."
            else:
                assert np.isnan(val), f"Expected NaN for feature {i+1} when testing ts containing {val_type}, got {val}."
        
def test_individual_feature_methods():
    # ensure each indiviudal feature method can be run in isolation
    all_methods = dir(catch22)
    data = list(np.random.randn(100))
    methods = [getattr(catch22, method) for method in all_methods if callable(getattr(catch22, method))]
    methods = methods[:-1]
    assert len(methods) == 24, "Expected 24 individual feature methods."
    for method in methods:
        try:
            method(data)
        except Exception as excinfo:
            pytest.fail(f"Method {method.__name__} raised an exception: {excinfo}")
