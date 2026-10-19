<p align="center"><img src="img/catch22_logo_square.png" alt="catch22 logo" height="220"/></p>

<h1 align="center"><em>pycatch22</em>: CAnonical Time-series CHaracteristics in Python</h1>

<p align="center">
    <a href="https://www.gnu.org/licenses/gpl-3.0"><img src="https://img.shields.io/badge/License-GPLv3-blue.svg" height="20"/></a>
 	  <a href="https://twitter.com/compTimeSeries"><img src="https://img.shields.io/twitter/url/https/twitter.com/compTimeSeries.svg?style=social&label=Follow%20%40compTimeSeries" height="20"/></a><br>
    <a href="https://pepy.tech/projects/pycatch22"><img src="https://static.pepy.tech/personalized-badge/pycatch22?period=total&units=INTERNATIONAL_SYSTEM&left_color=GREY&right_color=BLUE&left_text=downloads" alt="pycatch22 downloads" height="20"/></a>
    <a href="https://pepy.tech/projects/pycatch22"><img src="https://static.pepy.tech/personalized-badge/pycatch22?period=monthly&units=INTERNATIONAL_SYSTEM&left_color=GREY&right_color=BLUE&left_text=downloads%2Fmonth" alt="pycatch22 downloads per month" height="20"/></a>
    <a href="https://anaconda.org/conda-forge/pycatch22"><img src="https://img.shields.io/conda/dn/conda-forge/pycatch22?label=conda%20downloads&color=blue" alt="pycatch22 conda downloads" height="20"/></a>
</p>


## About

[_catch22_](https://github.com/DynamicsAndNeuralSystems/catch22) is a collection of 22 time-series features coded in C that can be run from Python, as well as [R](https://github.com/hendersontrent/Rcatch22), [MATLAB](https://github.com/DynamicsAndNeuralSystems/catch22), and [Julia](https://github.com/brendanjohnharris/Catch22.jl).

This package provides a Python wrapper of the C code as the module _pycatch22_, which has no runtime dependencies. It is licensed under the [GNU GPL v3 license](http://www.gnu.org/licenses/gpl-3.0.html) (or later).

### What do the features do?

This [GitBook website](https://time-series-features.gitbook.io/catch22/feature-descriptions) is dedicated to describing the features.
For their implementation in code, see the [main _catch22_ repository](https://github.com/DynamicsAndNeuralSystems/catch22).
There is also information in the associated paper, &#x1F4D7; [Lubba et al. (2019)](https://doi.org/10.1007/s10618-019-00647-x).

### Acknowledgement :+1:

If you use this software, please read and cite this open-access article:

- &#x1F4D7; Lubba et al. [_catch22_: CAnonical Time-series CHaracteristics](https://doi.org/10.1007/s10618-019-00647-x), _Data Min Knowl Disc_ __33__, 1821 (2019).

## Installation

Using `pip` for [`pycatch22`](https://pypi.org/project/pycatch22/):

```bash
pip install pycatch22
```

_pycatch22_ supports Python 3.8 and later. If installation fails, upgrade `pip` (`python -m pip install --upgrade pip`) and check that a C compiler is available (it is needed to build from source).

It is also a [package on anaconda](https://anaconda.org/conda-forge/pycatch22) thanks to [@rpanai](https://github.com/rpanai), which you can install via `conda`:

```bash
conda install -c conda-forge pycatch22
```

or `mamba`:

```bash
mamba install -c conda-forge pycatch22
```

If neither works, see [Manual install](#manual-install) below.

## Usage

Each feature function can be accessed individually and takes any sequence of numbers (a list, tuple, or `numpy` array); invalid input raises a `TypeError`.
For example, for a time series `tsData` in Python:

```python
import random
import pycatch22
tsData = [random.gauss(0, 1) for _ in range(500)] # (or more interesting data!)
pycatch22.CO_f1ecac(tsData)
```

All features are bundled in the method `catch22_all`, which returns a dictionary with the entries `'names'` (feature names) and `'values'` (feature outputs).

Usage (computing 22 features: _catch22_):

```python
pycatch22.catch22_all(tsData)
```

Usage (computing 24 features: _catch24_ = _catch22_ + mean + standard deviation):

```python
pycatch22.catch22_all(tsData, catch24=True)
```

We also include a 'short name' for each feature for easier reference (as outlined in the GitBook [Feature overview table](https://time-series-features.gitbook.io/catch22/feature-descriptions/feature-overview-table)).
These short names can be included in the output from `catch22_all()` (as the entry `'short_names'`) by setting `short_names=True` as follows:

```python
pycatch22.catch22_all(tsData, catch24=True, short_names=True)
```

### Template analysis script

Thanks to [@jmoo2880](https://github.com/jmoo2880) for putting together a [demonstration notebook](https://github.com/jmoo2880/c22-usage-examples/) for using pycatch22 to extract features from a time-series dataset.

### Usage notes

- When presenting results using _catch22_, you must identify the version used to allow clear reproduction of your results. For example, `CO_f1ecac` was altered from an integer-valued output to a linearly interpolated real-valued output from v0.3.
  From _pycatch22_ v0.6.0 (which uses _catch22_ v0.6.0), four features were corrected to match their MATLAB (_hctsa_) definitions, so their values differ from earlier versions: `PD_PeriodicityWang_th0_01` and `IN_AutoMutualInfoStats_40_gaussian_fmmi` now return the lag itself (previously the lag minus one), and `SB_BinaryStats_mean_longstretch1` and `SB_BinaryStats_diff_longstretch0` now return exact run lengths (previously one more for runs not at the start of the series).
  Also from v0.6.0, the short names `transition_matrix` and `SD` were renamed `transition_variance` and `std`, to match the other _catch22_ implementations.
- **Note:** _catch22_ features only evaluate _dynamical_ properties of time series and do not respond to basic differences in the location (e.g., mean) or spread (e.g., variance).
  - From _catch22_ v0.3, if the location and spread of the raw time-series distribution may be important for your application, we suggest applying the function argument `catch24 = True` to your call to the _catch22_ function in the language of your choice.
  This will result in 24 features being calculated: the _catch22_ features in addition to mean and standard deviation.

### Manual install

The upstream _catch22_ C sources are included as a git submodule, so clone with submodules before building from source:

```bash
git clone --recurse-submodules https://github.com/DynamicsAndNeuralSystems/pycatch22.git
```

(If you already cloned without `--recurse-submodules`, run `git submodule update --init` from the repository root.)

Then install from the cloned directory (this compiles the C code, so needs a C compiler):

```bash
pip install .
```
