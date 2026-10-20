<p align="center"><img src="https://raw.githubusercontent.com/DynamicsAndNeuralSystems/pycatch22/main/img/catch22_logo_square.png" alt="catch22 logo" height="200"/></p>

<h1 align="center"><em>pycatch22</em>: CAnonical Time-series CHaracteristics in Python</h1>

<p align="center">
  <a href="https://pypi.org/project/pycatch22/"><img src="https://img.shields.io/pypi/v/pycatch22?label=PyPI" alt="PyPI"/></a>
  <a href="https://doi.org/10.1007/s10618-019-00647-x"><img src="https://img.shields.io/badge/paper-Data%20Min%20Knowl%20Disc%20(2019)-informational" alt="Paper"/></a>
  <a href="https://www.gnu.org/licenses/gpl-3.0"><img src="https://img.shields.io/badge/license-GPLv3-blue.svg" alt="License: GPL v3"/></a>
  <a href="https://time-series-features.gitbook.io/catch22/language-specific-docs/python"><img src="https://img.shields.io/badge/docs-GitBook-blue" alt="Documentation"/></a>
  <a href="https://github.com/DynamicsAndNeuralSystems/pycatch22/actions/workflows/run_unit_tests.yaml"><img src="https://github.com/DynamicsAndNeuralSystems/pycatch22/actions/workflows/run_unit_tests.yaml/badge.svg" alt="Tests"/></a>
  <a href="https://github.com/DynamicsAndNeuralSystems/pycatch22/actions/workflows/wheels.yml"><img src="https://github.com/DynamicsAndNeuralSystems/pycatch22/actions/workflows/wheels.yml/badge.svg" alt="Wheels"/></a>
  <br>
  <a href="https://pepy.tech/projects/pycatch22"><img src="https://static.pepy.tech/personalized-badge/pycatch22?period=total&units=INTERNATIONAL_SYSTEM&left_color=GREY&right_color=BLUE&left_text=downloads" alt="pycatch22 downloads"/></a>
  <a href="https://pepy.tech/projects/pycatch22"><img src="https://static.pepy.tech/personalized-badge/pycatch22?period=monthly&units=INTERNATIONAL_SYSTEM&left_color=GREY&right_color=BLUE&left_text=downloads%2Fmonth" alt="pycatch22 downloads per month"/></a>
  <a href="https://anaconda.org/conda-forge/pycatch22"><img src="https://img.shields.io/conda/dn/conda-forge/pycatch22?label=conda%20downloads&color=blue" alt="pycatch22 conda downloads"/></a>
</p>

_pycatch22_ computes the [_catch22_](https://github.com/DynamicsAndNeuralSystems/catch22) time-series features in Python.
_catch22_ is a set of 22 features, selected from the more than 7000 in [_hctsa_](https://github.com/benfulcher/hctsa) for their classification performance across 93 time-series classification problems ([Lubba et al., 2019](https://doi.org/10.1007/s10618-019-00647-x)).
They capture a time series's dynamics, such as its autocorrelation, distribution of values, extreme events, scaling and predictability, and are fast to compute.
_pycatch22_ wraps the _catch22_ C code, and has no runtime dependencies.

📖 **Full documentation:** the [Python guide](https://time-series-features.gitbook.io/catch22/language-specific-docs/python), and [what each feature measures](https://time-series-features.gitbook.io/catch22/information-about-catch22/feature-descriptions).

## Installation

```bash
pip install pycatch22
```

Pre-built wheels are available for Python 3.9 and later on Linux, macOS and Windows.
Elsewhere (e.g., Python 3.8), `pip` builds _pycatch22_ from source, which needs a C compiler.

_pycatch22_ is also on [conda-forge](https://anaconda.org/conda-forge/pycatch22), thanks to [@rpanai](https://github.com/rpanai), although it can lag behind PyPI:

```bash
conda install -c conda-forge pycatch22
```

<details>
<summary>Installing from source</summary>

The _catch22_ C code is a git submodule, so clone with submodules, then install (this needs a C compiler):

```bash
git clone --recurse-submodules https://github.com/DynamicsAndNeuralSystems/pycatch22.git
cd pycatch22
pip install .
```

If you already cloned without `--recurse-submodules`, run `git submodule update --init` first.

</details>

## Quick start

```python
import numpy as np
import pycatch22

x = np.sin(np.arange(500) * 2 * np.pi / 50) + 0.5 * np.random.default_rng(1).standard_normal(500)

results = pycatch22.catch22_all(x)  # a dict of 'names' and 'values'
features = dict(zip(results['names'], results['values']))
```

`catch22_all` takes any sequence of numbers (a list, tuple or `numpy` array), and returns the feature names and their values (as floats).
Select features by name rather than by position.

## Options

| Option | Effect |
|---|---|
| `catch24=True` | Also compute the mean and standard deviation (_catch24_; see below) |
| `short_names=True` | Also return `'short_names'`, e.g., `acf_timescale` for `CO_FirstCrossing_acf_1e_pointOfCrossing` |
| `mask_nans=False` | Return `NaN` for features that cannot be estimated, instead of masking them (see below) |
| `return_masked=True` | Also return `'masked'`, which says which values were masked |

For example:

```python
results = pycatch22.catch22_all(x, catch24=True, short_names=True)
# short_names: ['mode_5', 'mode_10', 'outlier_timing_pos', 'outlier_timing_neg', 'acf_timescale', ...]
# values:      [-0.1257, -0.8436, 0.032, -0.044, 7.896, ...] (rounded)
```

**Single features.**
Compute one feature by its long or short name, or with its own function (both give exactly the value `catch22_all` gives, computing only that feature):

```python
pycatch22.compute_feature(x, 'acf_first_min')
pycatch22.CO_FirstMin_ac(x)
```

**The feature table.**
`pycatch22.feature_table()` lists each feature's name, short name, name before v1.0, and the _hctsa_ code that reproduces it:

```python
pycatch22.feature_table()[4]
# {'name': 'CO_FirstCrossing_acf_1e_pointOfCrossing', 'short_name': 'acf_timescale', 'legacy_name': 'CO_f1ecac',
#  'hctsa_call': "CO_FirstCrossing(x_z,'ac',1/exp(1),'both').pointOfCrossing"}
```

**Many time series.**
_pycatch22_ releases Python's global interpreter lock while it computes, so threads (e.g., a `concurrent.futures.ThreadPoolExecutor`) compute the features of different time series in parallel.

For a worked example on a dataset, see [@jmoo2880](https://github.com/jmoo2880)'s [demonstration notebook](https://github.com/jmoo2880/c22-usage-examples/).

## Usage notes

- **Location and spread.**
  Each time series is _z_-scored before the 22 features are computed, so they measure its dynamics and are insensitive to its mean and variance.
  If the mean and spread matter for your application, use `catch24=True`, which adds the mean and standard deviation.
- **Features that cannot be estimated** (e.g., for a constant series, or `dfa` on a series shorter than 79 samples) are _masked_ by default: set to a fixed value at the appropriate end of their range, so you always get 22 real numbers.
  Use `mask_nans=False` to get `NaN` instead.
  A series containing `NaN` or `Inf` gives `NaN` for every feature, with a warning.
- **Sampling.**
  A time series is an ordered sequence of values without time stamps, assumed to be evenly sampled.

## Versions

Feature values can change between versions, so **report the version of _pycatch22_ you used** so that your results can be reproduced.

- **v1.0** (using [_catch22_ v1.1.0](https://github.com/DynamicsAndNeuralSystems/catch22/releases/tag/v1.1.0)): every feature now exactly reproduces its definition in [_hctsa_ v3.0.0](https://github.com/benfulcher/hctsa/tree/v3.0.0), so values change for most features.
  Several features are renamed (e.g., `CO_f1ecac` is now `CO_FirstCrossing_acf_1e_pointOfCrossing`, and `centroid_freq` is replaced by the median frequency, `median_freq`); the old function names still work, but are deprecated.
  Features that cannot be estimated are masked by default, all values are floats, and features are returned in _catch22_'s order (which differs from earlier versions).
  See the [_catch22_ v1.0.0 release notes](https://github.com/DynamicsAndNeuralSystems/catch22/releases/tag/v1.0.0) for how each feature changed.
- **v0.6.0:** four features were corrected to match their _hctsa_ definitions (`PD_PeriodicityWang_th0_01`, `IN_AutoMutualInfoStats_40_gaussian_fmmi`, `SB_BinaryStats_mean_longstretch1` and `SB_BinaryStats_diff_longstretch0`), and the short names `transition_matrix` and `SD` became `transition_variance` and `std`.
- **v0.3:** `CO_f1ecac` changed from an integer to a linearly interpolated real value.

See the [releases](https://github.com/DynamicsAndNeuralSystems/pycatch22/releases) for details.

## Citing _catch22_

If you use _pycatch22_, please cite the open-access paper:

> C. H. Lubba, S. S. Sethi, P. Knaute, S. R. Schultz, B. D. Fulcher, N. S. Jones.
> [_catch22_: CAnonical Time-series CHaracteristics](https://doi.org/10.1007/s10618-019-00647-x).
> _Data Mining and Knowledge Discovery_ **33**, 1821–1852 (2019).

<details>
<summary>BibTeX</summary>

```bibtex
@article{lubba2019catch22,
  title   = {catch22: {CA}nonical {T}ime-series {CH}aracteristics},
  author  = {Lubba, Carl H. and Sethi, Sarab S. and Knaute, Philip and Schultz, Simon R. and Fulcher, Ben D. and Jones, Nick S.},
  journal = {Data Mining and Knowledge Discovery},
  volume  = {33},
  number  = {6},
  pages   = {1821--1852},
  year    = {2019},
  doi     = {10.1007/s10618-019-00647-x}
}
```

</details>

## License

_pycatch22_ is licensed under the [GNU GPL v3](http://www.gnu.org/licenses/gpl-3.0.html) (or later).
