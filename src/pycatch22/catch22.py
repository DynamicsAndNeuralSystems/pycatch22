from __future__ import annotations

from typing import Sequence, Union

import numpy as np

import catch22_C

ArrayLike = Union[Sequence[float], np.ndarray]

# (full name, short name) for each feature, in canonical output order.
_CATCH22_FEATURES = (
    ('DN_HistogramMode_5', 'mode_5'),
    ('DN_HistogramMode_10', 'mode_10'),
    ('CO_f1ecac', 'acf_timescale'),
    ('CO_FirstMin_ac', 'acf_first_min'),
    ('CO_HistogramAMI_even_2_5', 'ami2'),
    ('CO_trev_1_num', 'trev'),
    ('MD_hrv_classic_pnn40', 'high_fluctuation'),
    ('SB_BinaryStats_mean_longstretch1', 'stretch_high'),
    ('SB_TransitionMatrix_3ac_sumdiagcov', 'transition_matrix'),
    ('PD_PeriodicityWang_th0_01', 'periodicity'),
    ('CO_Embed2_Dist_tau_d_expfit_meandiff', 'embedding_dist'),
    ('IN_AutoMutualInfoStats_40_gaussian_fmmi', 'ami_timescale'),
    ('FC_LocalSimple_mean1_tauresrat', 'whiten_timescale'),
    ('DN_OutlierInclude_p_001_mdrmd', 'outlier_timing_pos'),
    ('DN_OutlierInclude_n_001_mdrmd', 'outlier_timing_neg'),
    ('SP_Summaries_welch_rect_area_5_1', 'low_freq_power'),
    ('SB_BinaryStats_diff_longstretch0', 'stretch_decreasing'),
    ('SB_MotifThree_quantile_hh', 'entropy_pairs'),
    ('SC_FluctAnal_2_rsrangefit_50_1_logi_prop_r1', 'rs_range'),
    ('SC_FluctAnal_2_dfa_50_1_2_logi_prop_r1', 'dfa'),
    ('SP_Summaries_welch_rect_centroid', 'centroid_freq'),
    ('FC_LocalSimple_mean3_stderr', 'forecast_error'),
)

# The two extra features that promote catch22 to catch24.
_CATCH24_EXTRA_FEATURES = (
    ('DN_Mean', 'mean'),
    ('DN_Spread_Std', 'SD'),
)


def catch22_all(
    data: ArrayLike,
    catch24: bool = False,
    short_names: bool = False,
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

    '''

    feature_set = _CATCH22_FEATURES + _CATCH24_EXTRA_FEATURES if catch24 else _CATCH22_FEATURES

    data = list(data)
    names = [name for name, _ in feature_set]
    values = [getattr(catch22_C, name)(data) for name in names]

    output = {'names': names, 'values': values}
    if short_names:
        output['short_names'] = [short for _, short in feature_set]

    return output
