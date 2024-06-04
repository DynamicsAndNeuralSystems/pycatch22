import pycatch22 as catch22
import pytest
import numpy as np
import pandas as pd

# unit tests
def expected_output(res, catch24=False):
    which_set = "Catch24" if catch24 else "Catch22"
    num_features = 24 if catch24 else 22
    # check if the output is a dictionary
    assert isinstance(res, pd.DataFrame), f"{which_set} did not return a DataFrame. Unexpected output."
    # check if the dataframe has three columns - features, values and hctsa_names
    assert len(res.columns) == 3, f"{which_set} returned a DataFrame with an unexpected number of columns."
    assert all(col_name in ['feature', 'value', 'hctsa_name'] for col_name in res.columns), f"{which_set} returned unexpected columns."
    # check the column datatypes
    assert all(isinstance(fname, str) for fname in res.feature), f"{which_set} expected all returned feature names to be strings."
    length_of_names = len(res.feature)
    assert length_of_names == num_features, f"Expected {num_features} names for {which_set}, got {length_of_names} instead."

    # check the 'value' column
    length_of_vals = len(res.value)
    assert length_of_vals == num_features, f"Expected {num_features} values for {which_set}, got {length_of_vals} instead."
    assert all(isinstance(val, (float, int)) for val in res.value), f"{which_set} expected all returned feature values to be floats or integers."

    # check the `hctsa_name` column
    length_of_hctsa_names = len(res.hctsa_name)
    assert length_of_hctsa_names == num_features, f"Expected {num_features} hctsa names for {which_set}, got {length_of_hctsa_names} instead."
    assert all(isinstance(fname, str) for fname in res.hctsa_name), f"{which_set} expected all returned hctsa feature names to be strings."

def test_catch22_runs():
    # test whether catch22 works on some random data
    tsData = np.random.randn(100)
    res = catch22.catch22_all(tsData, catch24=False)
    expected_output(res, catch24=False)

def test_catch24_runs():
    # test whether catch24 works on some random data
    tsData = np.random.randn(100)
    res = catch22.catch22_all(tsData, catch24=True)
    expected_output(res, catch24=True)
   
def test_short_names_returned():
    # test whether catch22/catch24 returns short names
    tsData = np.random.randn(100)
    res = catch22.catch22_all(tsData, catch24=False)
    expected_output(res, catch24=False)
    res2 = catch22.catch22_all(tsData, catch24=True)
    expected_output(res2, catch24=True)

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
        expected_output(res, catch24=False)
        res_values = res['value']
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
