import math
import os
import warnings

import numpy as np
import pytest

import pycatch22 as catch22


# unit tests
def expected_output(res, catch24=False, short_names=False, return_masked=False):
    which_set = "Catch24" if catch24 else "Catch22"
    num_features = 24 if catch24 else 22
    assert isinstance(res, dict), f"{which_set} did not return a dictionary."
    expected_keys = {'names', 'values'} | ({'short_names'} if short_names else set()) | ({'masked'} if return_masked else set())
    assert set(res.keys()) == expected_keys, f"{which_set} returned keys {sorted(res.keys())}, expected {sorted(expected_keys)}."
    for key in expected_keys:
        assert isinstance(res[key], list), f"{which_set}: '{key}' is not a list."
        assert len(res[key]) == num_features, f"{which_set}: expected {num_features} entries in '{key}', got {len(res[key])}."
    assert all(isinstance(name, str) for name in res['names'])
    assert all(isinstance(val, float) for val in res['values']), f"{which_set} expected all feature values to be floats."
    if short_names:
        assert all(isinstance(name, str) for name in res['short_names'])
    if return_masked:
        assert all(isinstance(m, bool) for m in res['masked'])

def test_catch22_runs():
    res = catch22.catch22_all(np.random.randn(100))
    expected_output(res)

def test_catch24_runs():
    res = catch22.catch22_all(np.random.randn(100), catch24=True)
    expected_output(res, catch24=True)

def test_optional_outputs():
    data = np.random.randn(100)
    for catch24 in (False, True):
        expected_output(catch22.catch22_all(data, catch24=catch24, short_names=True), catch24=catch24, short_names=True)
        expected_output(catch22.catch22_all(data, catch24=catch24, return_masked=True), catch24=catch24, return_masked=True)

def test_valid_input_types():
    # tuples, lists, numpy arrays and ranges all work, and give identical values
    data = list(np.random.randn(100))
    vals = catch22.catch22_all(data, catch24=True)['values']
    assert catch22.catch22_all(tuple(data), catch24=True)['values'] == vals
    assert catch22.catch22_all(np.array(data), catch24=True)['values'] == vals
    expected_output(catch22.catch22_all(range(50)))

def test_inf_and_nan_input():
    # a time series containing NaN or Inf gives NaN for every feature (never masked), with a warning
    for bad_value in (np.nan, np.inf, -np.inf):
        data = np.random.randn(100)
        data[0] = bad_value
        with pytest.warns(RuntimeWarning):
            res = catch22.catch22_all(data, catch24=True, return_masked=True)
        expected_output(res, catch24=True, return_masked=True)
        assert all(math.isnan(v) for v in res['values']), f"Expected all NaN for a series containing {bad_value}."
        assert not any(res['masked'])

def test_constant_series_is_masked():
    # a constant series cannot be z-scored: masked values by default, NaN without masking
    data = [3.0] * 100
    res = catch22.catch22_all(data, catch24=True, return_masked=True)
    values = dict(zip(res['names'], res['values']))
    assert res['masked'][:22] == [True] * 22 and res['masked'][22:] == [False, False]
    assert not any(math.isnan(v) for v in res['values'])
    assert values['DN_mean'] == 3.0 and values['DN_Spread_std'] == 0.0
    res = catch22.catch22_all(data, catch24=True, mask_nans=False)
    assert all(math.isnan(v) for v in res['values'][:22])

def test_masking_only_replaces_nans():
    # on a series where every feature can be estimated, masking changes nothing
    data = np.random.randn(500)
    res = catch22.catch22_all(data, catch24=True, return_masked=True)
    assert not any(res['masked'])
    assert res['values'] == catch22.catch22_all(data, catch24=True, mask_nans=False)['values']

def test_short_series_masked_features():
    # dfa needs at least 79 samples (as in hctsa): masked below that, NaN without masking
    data = np.random.randn(60)
    res = catch22.catch22_all(data, return_masked=True)
    i = res['names'].index('SC_FluctAnal_2_dfa_50_1_2_logi_prop_r1')
    assert res['masked'][i]
    assert math.isnan(catch22.catch22_all(data, mask_nans=False)['values'][i])

def test_deterministic_output():
    data = np.random.randn(100)
    assert catch22.catch22_all(data, catch24=True) == catch22.catch22_all(data, catch24=True)

def test_input_not_mutated():
    data = np.random.randn(100)
    data_copy = data.copy()
    catch22.catch22_all(data, catch24=True)
    assert np.array_equal(data, data_copy)

def test_catch24_is_superset_of_catch22():
    data = np.random.randn(100)
    res22 = catch22.catch22_all(data)
    res24 = catch22.catch22_all(data, catch24=True)
    assert res24['names'][:22] == res22['names']
    assert res24['values'][:22] == res22['values']
    assert res24['names'][22:] == ['DN_mean', 'DN_Spread_std']

def test_catch24_mean_and_std_values():
    data = np.random.randn(500)
    values = dict(zip(*catch22.catch22_all(data, catch24=True).values()))
    assert np.isclose(values['DN_mean'], np.mean(data))
    assert np.isclose(values['DN_Spread_std'], np.std(data, ddof=1))

def test_individual_feature_functions():
    # one function per feature, named as in catch22_all, giving the same value
    data = list(np.random.randn(200))
    res = catch22.catch22_all(data, catch24=True)
    assert set(res['names']) <= set(catch22.__all__)
    for name, val in zip(res['names'], res['values']):
        individual = getattr(catch22, name)(data)
        assert individual == val or (math.isnan(val) and math.isnan(individual)), f"{name}: {individual} vs catch22_all {val}."
        assert getattr(catch22, name)(np.array(data)) == individual

def test_individual_feature_functions_on_edge_cases():
    # same values as catch22_all where features are masked (or NaN without masking)
    for data in ([3.0] * 50, list(np.random.randn(60)), [2.0]):
        for mask_nans in (True, False):
            res = catch22.catch22_all(data, catch24=True, mask_nans=mask_nans)
            for name, val in zip(res['names'], res['values']):
                individual = getattr(catch22, name)(data, mask_nans=mask_nans)
                assert individual == val or (math.isnan(val) and math.isnan(individual)), f"{name}: {individual} vs catch22_all {val}."
    with pytest.warns(RuntimeWarning):
        assert math.isnan(catch22.CO_trev_1_num([1.0, np.nan, 2.0]))

def test_compute_feature_by_name():
    # by long or short name, the same value as catch22_all
    data = list(np.random.randn(200))
    res = catch22.catch22_all(data, catch24=True, short_names=True)
    for name, short, val in zip(res['names'], res['short_names'], res['values']):
        assert catch22.compute_feature(data, name) == val
        assert catch22.compute_feature(data, short) == val
    assert math.isnan(catch22.compute_feature([3.0] * 50, 'trev', mask_nans=False))
    for bad_name in ('not_a_feature', 'CO_f1ecac'):
        with pytest.raises(ValueError):
            catch22.compute_feature(data, bad_name)

def test_legacy_names_are_deprecated_aliases():
    data = list(np.random.randn(200))
    for row in catch22.feature_table(catch24=True):
        if row['legacy_name'] == row['name']:
            continue
        with pytest.warns(DeprecationWarning):
            assert getattr(catch22, row['legacy_name'])(data) == getattr(catch22, row['name'])(data)

def test_invalid_input_raises_type_error():
    for bad_input in (None, 3.0, [1.0, 'a', 3.0]):
        with pytest.raises(TypeError):
            catch22.catch22_all(bad_input)
        with pytest.raises(TypeError):
            catch22.CO_FirstMin_ac(bad_input)

def test_lag_features_are_integer_valued_floats():
    data = list(np.sin(np.arange(200) * 2 * np.pi / 20))
    assert catch22.PD_PeriodicityWang_th0_01(data) == 20.0
    assert catch22.CO_FirstMin_ac(data) == 10.0

def test_feature_table_matches_upstream_feature_list():
    # names, short names, legacy names and hctsa calls match catch22's featureList.txt
    feature_list = os.path.join(os.path.dirname(__file__), '..', 'src', 'catch22', 'featureList.txt')
    if not os.path.exists(feature_list):
        pytest.skip("catch22 submodule not checked out")
    with open(feature_list) as f:
        rows = [line.rstrip('\n').split('\t') for line in f if line.strip() and not line.startswith('#')]
    header, rows = rows[0], rows[1:]
    assert header == ['name', 'short_name', 'legacy_name', 'hctsa_call']
    table = catch22.feature_table(catch24=True)
    assert [[row[k] for k in header] for row in table] == rows
    res = catch22.catch22_all(np.random.randn(100), catch24=True, short_names=True)
    assert res['names'] == [row['name'] for row in table]
    assert res['short_names'] == [row['short_name'] for row in table]

def test_no_warning_for_valid_input():
    with warnings.catch_warnings():
        warnings.simplefilter('error')
        catch22.catch22_all(np.random.randn(100), catch24=True)
