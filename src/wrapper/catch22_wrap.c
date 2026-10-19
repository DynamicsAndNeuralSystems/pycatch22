#include <Python.h>

// include functions
#include "CO_AutoCorr.h"
#include "DN_HistogramMode_10.h"
#include "DN_HistogramMode_5.h"
#include "DN_Mean.h"
#include "DN_Spread_Std.h"
#include "DN_OutlierInclude.h"
#include "FC_LocalSimple.h"
#include "IN_AutoMutualInfoStats.h"
#include "MD_hrv.h"
#include "PD_PeriodicityWang.h"
#include "SB_BinaryStats.h"
#include "SB_CoarseGrain.h"
#include "SB_MotifThree.h"
#include "SB_TransitionMatrix.h"
#include "SC_FluctAnal.h"
#include "SP_Summaries.h"
#include "butterworth.h"
#include "fft.h"
#include "helper_functions.h"
#include "histcounts.h"
#include "splinefit.h"
#include "stats.h"


// ---------------------------------------------------------------------
// -------------------- Main wrapper function --------------------------
// ---------------------------------------------------------------------

// used for all functions to wrap via a function handle

// Read the single argument (any sequence of numbers: list, tuple, numpy
// array, range, ...) into a newly allocated C array. Returns NULL with a
// Python exception set on failure; on success the caller frees the array.
static double * parse_input(PyObject * args, int * n)
{
    PyObject * py_input;

    // parse arguments
    if(!PyArg_ParseTuple(args, "O", &py_input)){
       return NULL;
    }

    PyObject * seq = PySequence_Fast(py_input, "input must be a sequence of numbers (e.g., a list, tuple, or numpy array)");
    if (seq == NULL){
        return NULL;
    }

    *n = (int) PySequence_Fast_GET_SIZE(seq);
    PyObject ** items = PySequence_Fast_ITEMS(seq);

    // allocate space for input array (C data format); at least one element so
    // that malloc never returns NULL for an empty input
    double * c_array = malloc((*n > 0 ? *n : 1) * sizeof * c_array);
    if (c_array == NULL){
        Py_DECREF(seq);
        PyErr_NoMemory();
        return NULL;
    }

    // write input array to c array
    for (int i = 0; i < *n; i++) {
        c_array[i] = PyFloat_AsDouble(items[i]);
        if (c_array[i] == -1.0 && PyErr_Occurred()){
            free(c_array);
            Py_DECREF(seq);
            return NULL;
        }
    }

    Py_DECREF(seq);
    return c_array;
}

// Copy the input (z-scored if normalize) into a new array for the feature
// function, so that the input is never altered.
static double * prepare_input(const double * c_array, const int n, int normalize)
{
    double * y = malloc((n > 0 ? n : 1) * sizeof * y);
    if (y == NULL){
        return NULL;
    }
    if (normalize){
        zscore_norm2(c_array, n, y);
    }
    else {
        memcpy(y, c_array, n * sizeof * y);
    }
    return y;
}

static PyObject * python_wrapper_double(PyObject * args, double (*f) (const double*, const int), int normalize)
{
    int n;
    double * c_array = parse_input(args, &n);
    if (c_array == NULL){
        return NULL;
    }

    double * y = prepare_input(c_array, n, normalize);
    free(c_array);
    if (y == NULL){
        return PyErr_NoMemory();
    }

    double result = f(y, n);
    free(y);

    return Py_BuildValue("d", result);
};

static PyObject * python_wrapper_int(PyObject * args, int (*f) (const double*, const int), int normalize)
{
    int n;
    double * c_array = parse_input(args, &n);
    if (c_array == NULL){
        return NULL;
    }

    double * y = prepare_input(c_array, n, normalize);
    free(c_array);
    if (y == NULL){
        return PyErr_NoMemory();
    }

    int result = f(y, n);
    free(y);

    return Py_BuildValue("i", result);
};


// ---------------------------------------------------------------------
// ----------------------- Functions to wrap ---------------------------
// ---------------------------------------------------------------------

static PyObject * DN_HistogramMode_5_wrapper(PyObject * self, PyObject * args)
{
    return python_wrapper_double(args, &DN_HistogramMode_5, 1);
}

static PyObject * DN_HistogramMode_10_wrapper(PyObject * self, PyObject * args)
{
    return python_wrapper_double(args, &DN_HistogramMode_10, 1);
}

static PyObject * DN_Mean_wrapper(PyObject * self, PyObject * args)
{
    return python_wrapper_double(args, &DN_Mean, 0);
}

static PyObject * DN_Spread_Std_wrapper(PyObject * self, PyObject * args)
{
    return python_wrapper_double(args, &DN_Spread_Std, 0);
}

static PyObject * CO_f1ecac_wrapper(PyObject * self, PyObject * args)
{
    return python_wrapper_double(args, &CO_f1ecac, 1);
}

static PyObject * CO_FirstMin_ac_wrapper(PyObject * self, PyObject * args)
{
    return python_wrapper_int(args, &CO_FirstMin_ac, 1);
}

static PyObject * CO_HistogramAMI_even_2_5_wrapper(PyObject * self, PyObject * args)
{
    return python_wrapper_double(args, &CO_HistogramAMI_even_2_5, 1);
}

static PyObject * CO_trev_1_num_wrapper(PyObject * self, PyObject * args)
{
    return python_wrapper_double(args, &CO_trev_1_num, 1);
}

static PyObject * MD_hrv_classic_pnn40_wrapper(PyObject * self, PyObject * args)
{
    return python_wrapper_double(args, &MD_hrv_classic_pnn40, 1);
}

static PyObject * SB_BinaryStats_mean_longstretch1_wrapper(PyObject * self, PyObject * args)
{
    return python_wrapper_double(args, &SB_BinaryStats_mean_longstretch1, 1);
}

static PyObject * SB_TransitionMatrix_3ac_sumdiagcov_wrapper(PyObject * self, PyObject * args)
{
    return python_wrapper_double(args, &SB_TransitionMatrix_3ac_sumdiagcov, 1);
}

static PyObject * PD_PeriodicityWang_th0_01_wrapper(PyObject * self, PyObject * args)
{
    return python_wrapper_int(args, &PD_PeriodicityWang_th0_01, 1);
}

static PyObject * CO_Embed2_Dist_tau_d_expfit_meandiff_wrapper(PyObject * self, PyObject * args)
{
    return python_wrapper_double(args, &CO_Embed2_Dist_tau_d_expfit_meandiff, 1);
}

static PyObject * IN_AutoMutualInfoStats_40_gaussian_fmmi_wrapper(PyObject * self, PyObject * args)
{
    return python_wrapper_double(args, &IN_AutoMutualInfoStats_40_gaussian_fmmi, 1);
}

static PyObject * FC_LocalSimple_mean1_tauresrat_wrapper(PyObject * self, PyObject * args)
{
    return python_wrapper_double(args, &FC_LocalSimple_mean1_tauresrat, 1);
}

static PyObject * DN_OutlierInclude_p_001_mdrmd_wrapper(PyObject * self, PyObject * args)
{
    return python_wrapper_double(args, &DN_OutlierInclude_p_001_mdrmd, 1);
}

static PyObject * DN_OutlierInclude_n_001_mdrmd_wrapper(PyObject * self, PyObject * args)
{
    return python_wrapper_double(args, &DN_OutlierInclude_n_001_mdrmd, 1);
}

static PyObject * SP_Summaries_welch_rect_area_5_1_wrapper(PyObject * self, PyObject * args)
{
    return python_wrapper_double(args, &SP_Summaries_welch_rect_area_5_1, 1);
}

static PyObject * SB_BinaryStats_diff_longstretch0_wrapper(PyObject * self, PyObject * args)
{
    return python_wrapper_double(args, &SB_BinaryStats_diff_longstretch0, 1);
}

static PyObject * SB_MotifThree_quantile_hh_wrapper(PyObject * self, PyObject * args)
{
    return python_wrapper_double(args, &SB_MotifThree_quantile_hh, 1);
}

static PyObject * SC_FluctAnal_2_rsrangefit_50_1_logi_prop_r1_wrapper(PyObject * self, PyObject * args)
{
    return python_wrapper_double(args, &SC_FluctAnal_2_rsrangefit_50_1_logi_prop_r1, 1);
}

static PyObject * SC_FluctAnal_2_dfa_50_1_2_logi_prop_r1_wrapper(PyObject * self, PyObject * args)
{
    return python_wrapper_double(args, &SC_FluctAnal_2_dfa_50_1_2_logi_prop_r1, 1);
}

static PyObject * SP_Summaries_welch_rect_centroid_wrapper(PyObject * self, PyObject * args)
{
    return python_wrapper_double(args, &SP_Summaries_welch_rect_centroid, 1);
}

static PyObject * FC_LocalSimple_mean3_stderr_wrapper(PyObject * self, PyObject * args)
{
    return python_wrapper_double(args, &FC_LocalSimple_mean3_stderr, 1);
}

// ---------------------------------------------------------------------
// ------------------------ Module creation ----------------------------
// ---------------------------------------------------------------------

// register within a module
static PyMethodDef catch22Methods[] = {
    { "DN_HistogramMode_5", DN_HistogramMode_5_wrapper, METH_VARARGS, "bla" },
    { "DN_HistogramMode_10", DN_HistogramMode_10_wrapper, METH_VARARGS, "bla" },
    { "DN_Mean", DN_Mean_wrapper, METH_VARARGS, "bla" },
    { "DN_Spread_Std", DN_Spread_Std_wrapper, METH_VARARGS, "bla" },
    { "CO_f1ecac", CO_f1ecac_wrapper, METH_VARARGS, "bla" },
    { "CO_FirstMin_ac", CO_FirstMin_ac_wrapper, METH_VARARGS, "bla" },
    { "CO_HistogramAMI_even_2_5", CO_HistogramAMI_even_2_5_wrapper, METH_VARARGS, "bla" },
    { "CO_trev_1_num", CO_trev_1_num_wrapper, METH_VARARGS, "bla" },
    { "MD_hrv_classic_pnn40", MD_hrv_classic_pnn40_wrapper, METH_VARARGS, "bla" },
    { "SB_BinaryStats_mean_longstretch1", SB_BinaryStats_mean_longstretch1_wrapper, METH_VARARGS, "bla" },
    { "SB_TransitionMatrix_3ac_sumdiagcov", SB_TransitionMatrix_3ac_sumdiagcov_wrapper, METH_VARARGS, "bla" },
    { "PD_PeriodicityWang_th0_01", PD_PeriodicityWang_th0_01_wrapper, METH_VARARGS, "bla" },
    { "CO_Embed2_Dist_tau_d_expfit_meandiff", CO_Embed2_Dist_tau_d_expfit_meandiff_wrapper, METH_VARARGS, "bla" },
    { "IN_AutoMutualInfoStats_40_gaussian_fmmi", IN_AutoMutualInfoStats_40_gaussian_fmmi_wrapper, METH_VARARGS, "bla" },
    { "FC_LocalSimple_mean1_tauresrat", FC_LocalSimple_mean1_tauresrat_wrapper, METH_VARARGS, "bla" },
    { "DN_OutlierInclude_p_001_mdrmd", DN_OutlierInclude_p_001_mdrmd_wrapper, METH_VARARGS, "bla" },
    { "DN_OutlierInclude_n_001_mdrmd", DN_OutlierInclude_n_001_mdrmd_wrapper, METH_VARARGS, "bla" },
    { "SP_Summaries_welch_rect_area_5_1", SP_Summaries_welch_rect_area_5_1_wrapper, METH_VARARGS, "bla" },
    { "SB_BinaryStats_diff_longstretch0", SB_BinaryStats_diff_longstretch0_wrapper, METH_VARARGS, "bla" },
    { "SB_MotifThree_quantile_hh", SB_MotifThree_quantile_hh_wrapper, METH_VARARGS, "bla" },
    { "SC_FluctAnal_2_rsrangefit_50_1_logi_prop_r1", SC_FluctAnal_2_rsrangefit_50_1_logi_prop_r1_wrapper, METH_VARARGS, "bla" },
    { "SC_FluctAnal_2_dfa_50_1_2_logi_prop_r1", SC_FluctAnal_2_dfa_50_1_2_logi_prop_r1_wrapper, METH_VARARGS, "bla" },
    { "SP_Summaries_welch_rect_centroid", SP_Summaries_welch_rect_centroid_wrapper, METH_VARARGS, "bla" },
    { "FC_LocalSimple_mean3_stderr", FC_LocalSimple_mean3_stderr_wrapper, METH_VARARGS, "bla" },
    { NULL, NULL, 0, NULL }
};


static struct PyModuleDef catch22_Cmodule = {
    PyModuleDef_HEAD_INIT,
    "catch22_C",   /* name of module */
    "22 Canonical Time-series CHaracteristcs", /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    catch22Methods,
};

PyMODINIT_FUNC PyInit_catch22_C(void)
{
    return PyModule_Create(&catch22_Cmodule);
}
