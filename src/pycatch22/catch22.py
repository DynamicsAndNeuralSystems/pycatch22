from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, Callable, Sequence, Union

import catch22_C

# numpy is only needed for the type hint, so pycatch22 has no runtime dependencies
if TYPE_CHECKING:
    import numpy as np

    ArrayLike = Union[Sequence[float], np.ndarray]

# (name, short name, name before v1.0, hctsa call) for each feature, in output
# order, from the C library (so the names always match catch22's)
_CATCH24_FEATURES = tuple(catch22_C.features(True))
_N_CATCH22 = len(catch22_C.features(False))


def catch22_all(
    data: ArrayLike,
    catch24: bool = False,
    short_names: bool = False,
    mask_nans: bool = True,
    return_masked: bool = False,
) -> dict[str, list]:
    '''
    Extract the catch22 feature set from an input time series.

    Parameters
    ----------
    data : array_like
        Input time-series data.
    catch24 : bool, optional
        If True, include the two catch24 features (mean and standard deviation) in the output.
    short_names : bool, optional
        If True, also include the short names of the features in the output.
    mask_nans : bool, optional
        If True (default), a feature that cannot be estimated (e.g., for a constant or very
        short time series) is set to a fixed value at the appropriate end of its range, so that
        real numbers are always returned. If False, it is NaN. A time series containing NaN or
        Inf gives NaN for every feature either way.
    return_masked : bool, optional
        If True, also include 'masked': for each feature, whether its value was masked.

    Returns
    -------
    dict
        'names' (the feature names) and 'values' (floats), plus 'short_names' and 'masked'
        if requested.
    '''

    values, masked, ok = catch22_C.compute(data, catch24, mask_nans)
    if not ok:
        warnings.warn("the time series is empty or contains NaN/Inf; all features are NaN",
                      RuntimeWarning, stacklevel=2)

    features = _CATCH24_FEATURES[:len(values)]
    output = {'names': [f[0] for f in features], 'values': values}
    if short_names:
        output['short_names'] = [f[1] for f in features]
    if return_masked:
        output['masked'] = masked

    return output


def feature_table(catch24: bool = False) -> list[dict[str, str]]:
    '''
    Describe the features, in the order of catch22_all.

    Each feature has its 'name', 'short_name', 'legacy_name' (its name in catch22 v0.x;
    definitions have since changed to match hctsa, so values differ) and 'hctsa_call' (the
    hctsa v3.0.0 call that reproduces it exactly, on x_z, the z-scored series, or x, the raw
    series).
    '''
    keys = ('name', 'short_name', 'legacy_name', 'hctsa_call')
    n = len(_CATCH24_FEATURES) if catch24 else _N_CATCH22
    return [dict(zip(keys, f)) for f in _CATCH24_FEATURES[:n]]


def _single_feature(index: int, name: str) -> Callable[..., float]:
    def compute(data: ArrayLike, mask_nans: bool = True) -> float:
        values, _, _ = catch22_C.compute(data, index >= _N_CATCH22, mask_nans)
        return values[index]
    compute.__name__ = compute.__qualname__ = name
    compute.__doc__ = (f"Compute {name} ({_CATCH24_FEATURES[index][1]}) of a time series "
                       f"(computes all features: use catch22_all for more than one).")
    return compute


def _deprecated_alias(name: str, legacy_name: str, function: Callable[..., float]) -> Callable[..., float]:
    def compute(data: ArrayLike, mask_nans: bool = True) -> float:
        warnings.warn(f"{legacy_name} is now {name} (catch22 v1.0, which also changed its "
                      f"definition to match hctsa)", DeprecationWarning, stacklevel=2)
        return function(data, mask_nans)
    compute.__name__ = compute.__qualname__ = legacy_name
    compute.__doc__ = f"Deprecated name for {name}."
    return compute


# One function per feature, by its name (e.g., pycatch22.DN_HistogramMode_5(data)), and
# by its name before v1.0 where that differs (deprecated)
FEATURE_FUNCTIONS = {}
_LEGACY_FUNCTIONS = {}
for _i, (_name, _short, _legacy, _call) in enumerate(_CATCH24_FEATURES):
    FEATURE_FUNCTIONS[_name] = _single_feature(_i, _name)
    if _legacy != _name:
        _LEGACY_FUNCTIONS[_legacy] = _deprecated_alias(_name, _legacy, FEATURE_FUNCTIONS[_name])
globals().update(FEATURE_FUNCTIONS)
globals().update(_LEGACY_FUNCTIONS)
