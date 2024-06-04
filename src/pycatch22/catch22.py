import catch22_C
import pandas as pd

def catch22_all(data, catch24=False):
    '''
    Extract the catch22 feature set from an input time series.

    Parameters
    ----------
    data : array_like
        Input time-series data.
    catch24 : bool, optional
        If True, include the two catch24 features (mean and standard deviation) in the output.

    '''

    features_hctsa = [
        'DN_HistogramMode_5',
        'DN_HistogramMode_10',
        'CO_f1ecac',
        'CO_FirstMin_ac',
        'CO_HistogramAMI_even_2_5',
        'CO_trev_1_num',
        'MD_hrv_classic_pnn40',
        'SB_BinaryStats_mean_longstretch1',
        'SB_TransitionMatrix_3ac_sumdiagcov',
        'PD_PeriodicityWang_th0_01',
        'CO_Embed2_Dist_tau_d_expfit_meandiff',
        'IN_AutoMutualInfoStats_40_gaussian_fmmi',
        'FC_LocalSimple_mean1_tauresrat',
        'DN_OutlierInclude_p_001_mdrmd',
        'DN_OutlierInclude_n_001_mdrmd',
        'SP_Summaries_welch_rect_area_5_1',
        'SB_BinaryStats_diff_longstretch0',
        'SB_MotifThree_quantile_hh',
        'SC_FluctAnal_2_rsrangefit_50_1_logi_prop_r1',
        'SC_FluctAnal_2_dfa_50_1_2_logi_prop_r1',
        'SP_Summaries_welch_rect_centroid',
        'FC_LocalSimple_mean3_stderr'
    ]

    features = [
        'mode_5',
        'mode_10',
        'acf_timescale',
        'acf_first_min',
        'ami2',
        'trev',
        'high_fluctuation',
        'stretch_high',
        'transition_matrix',
        'periodicity',
        'embedding_dist',
        'ami_timescale',
        'whiten_timescale',
        'outlier_timing_pos',
        'outlier_timing_neg',
        'centroid_freq',
        'stretch_decreasing',
        'entropy_pairs',
        'rs_range',
        'dfa',
        'low_freq_power',
        'forecast_error'
    ]

    if catch24:
        features_hctsa.append('DN_Mean')
        features_hctsa.append('DN_Spread_Std')
        features.append('mean')
        features.append('SD')

    data = list(data)
    featureOut = []
    for f in features_hctsa:
        featureFun = getattr(catch22_C, f)
        featureOut.append(featureFun(data))

    # convert to a dataframe
    feature_results = pd.DataFrame({'feature': features, 'value': featureOut, 'hctsa_name': features_hctsa})

    return feature_results 
