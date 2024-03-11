import pycatch22 as catch22
import os
import pytest
import glob
import numpy as np

# define fixtures
def load_benchmark_datasets():
    """function to load the benchmarking datsets and return
     a dictionary of datasets, each with feature/output as a key/value pair"""
    benchmark_datasets = {}
    inputs_folder_path = 'tests/benchmarks/inputs/*'
    for file_path in glob.glob(inputs_folder_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                filename = os.path.basename(file_path).split('_')[0]
                try:
                    ts_data = np.loadtxt(file)
                    benchmark_datasets[filename] = ts_data
                except Exception as e:
                    print(f"Error loading data from {file_path}: {e}")
        else:
            print(f"File not found: {file_path}")
    return benchmark_datasets

def load_expected_outputs():
    """ function to load the expected benchmarking results
    and return a dictionary of lists."""
    expected_outputs = {}
    outputs_folder_path = 'tests/benchmarks/expected_outputs/*'
    for file_path in glob.glob(outputs_folder_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                filename = os.path.basename(file_path).split('_')[0]
                data_dict = {}
                try:
                    for line in file:
                        feature_output = line.strip().split(', ')
                        key, value = feature_output
                        data_dict[key] = float(value) # convert everything to floats for easier comparison (i.e., ints to floats)
                    expected_outputs[filename] = data_dict

                except Exception as e:
                    print(f"Error loading data from {file_path}: {e}")
        else:
            print(f"File not found: {file_path}")

    return expected_outputs

def compute_new_features():
    """Computes new feature outputs on same benchmarking dataset and
    then returns dictionary of datasets in the same format as
    the loaded expected outputs dictionary"""

    benchmark_datasets = load_benchmark_datasets()
    datasets = benchmark_datasets.keys()
    dataset_dicts = {}
    for dset in datasets:
        dataset_dict_single = {}
        print(f"Computing features for: {dset}...")
        test_data = benchmark_datasets[dset]
        res = catch22.catch22_all(test_data, catch24=True)
        for (name, val) in zip(res['names'], res['values']):
            dataset_dict_single[name] = float(val)
        dataset_dicts[dset] = dataset_dict_single

    return dataset_dicts

def generate_test_params():
    """Function to generate combinations of
    input, expected output for each dataset"""
    expected_outputs = load_expected_outputs()
    new_outputs = compute_new_features()
    params = []
    # each combination of dataset, expected_out, new_out
    for dset in expected_outputs.keys():
        params.append((dset, expected_outputs[dset], new_outputs[dset]))
    return params

params = generate_test_params()
def pytest_generate_tests(metafunc):
    """Create a hook to generate parameter combinations for 
    parameterised test."""
    if "dset" in metafunc.fixturenames:
        metafunc.parametrize("dset, exp_out, new_out", params)

def test_features(dset, exp_out, new_out):
    tol = 1E-12
    """Run the benchmarking tests"""
    assert len(exp_out.keys()) == 24, f"Expected 24 features in expected output for dataset: {dset}."
    assert len(new_out.keys()) == 24, f"Expected 24 features in new output for dataset: {dset}."
    features = exp_out.keys()
    diffs = {}
    for feature in features:
        #loop through each feature and calculate diff
        exp_val = np.nan_to_num(exp_out[feature], nan=0.0)  
        new_val = np.nan_to_num(new_out[feature], nan=0.0) 
        feature_diff = np.abs(exp_val - new_val) 
        diffs[feature] = feature_diff
    
    # get non-zero keys (if they exist)
    non_zero_diffs = {k: v for k, v in diffs.items() if v > tol}    
    if non_zero_diffs:
        non_zero_diffs_str = ", ".join([f"{k}: {v}" for k, v in non_zero_diffs.items()])
        pytest.fail(f"Non-zero feature differences found for dataset {dset}: {non_zero_diffs_str}")
