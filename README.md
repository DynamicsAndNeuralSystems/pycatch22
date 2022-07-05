# _pycatch22_ - CAnonical Time-series CHaracteristics in python

## About

[_catch22_](https://github.com/DynamicsAndNeuralSystems/catch22) is a collection of 22 time-series features coded in C that can be run from Python, R, Matlab, and Julia.

This package provides a python implementation.

For details about the features, see the [main _catch22_ repository](https://github.com/DynamicsAndNeuralSystems/catch22) and its [wiki](https://github.com/DynamicsAndNeuralSystems/catch22/wiki), or read the paper:

- [&#x1F4D7; Lubba et al. (2019). _catch22_: CAnonical Time-series CHaracteristics](https://doi.org/10.1007/s10618-019-00647-x).


## Usage notes

- When presenting results using _catch22_, you must identify the version used to allow clear reproduction of your results. For example, `CO_f1ecac` was altered from an integer-valued output to a linearly interpolated real-valued output from v0.3.
- __Important Note:__ _catch22_ features only evaluate _dynamical_ properties of time series and do not respond to basic differences in the location (e.g., mean) or spread (e.g., variance).
  - From _catch22_ v0.3, If the location and spread of the raw time-series distribution may be important for your application, we suggest applying the function argument `catch24 = True` to your call to the _catch22_ function in the language of your choice.
  This will result in 24 features being calculated: the _catch22_ features in addition to mean and standard deviation.
