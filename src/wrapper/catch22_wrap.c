#include <Python.h>

#include "catch22.h"

// Python bindings for catch22_compute() and catch22_compute_feature() (catch22.h),
// the entry points shared by every catch22 wrapper.

// Read a sequence of numbers (list, tuple, numpy array, range, ...) into a newly
// allocated C array. Returns NULL with a Python exception set on failure; on
// success the caller frees the array.
static double * parse_series(PyObject * py_input, int * n)
{
    PyObject * seq = PySequence_Fast(py_input, "input must be a sequence of numbers (e.g., a list, tuple, or numpy array)");
    if (seq == NULL){
        return NULL;
    }

    const Py_ssize_t size = PySequence_Fast_GET_SIZE(seq);
    if (size > INT_MAX){
        Py_DECREF(seq);
        PyErr_SetString(PyExc_ValueError, "the time series is too long");
        return NULL;
    }
    *n = (int) size;
    PyObject ** items = PySequence_Fast_ITEMS(seq);

    // at least one element so that malloc never returns NULL for an empty input
    double * y = malloc((*n > 0 ? *n : 1) * sizeof * y);
    if (y == NULL){
        Py_DECREF(seq);
        PyErr_NoMemory();
        return NULL;
    }

    for (int i = 0; i < *n; i++) {
        y[i] = PyFloat_AsDouble(items[i]);
        if (y[i] == -1.0 && PyErr_Occurred()){
            free(y);
            Py_DECREF(seq);
            return NULL;
        }
    }

    Py_DECREF(seq);
    return y;
}

// compute(data, catch24, mask_nans) -> (values, masked, ok)
static PyObject * compute_wrapper(PyObject * self, PyObject * args)
{
    PyObject * py_input;
    int catch24 = 0;
    int mask_nans = 1;
    if (!PyArg_ParseTuple(args, "O|pp", &py_input, &catch24, &mask_nans)){
        return NULL;
    }

    int n;
    double * y = parse_series(py_input, &n);
    if (y == NULL){
        return NULL;
    }

    double out[CATCH24_N_FEATURES];
    int masked[CATCH24_N_FEATURES];
    int status;
    Py_BEGIN_ALLOW_THREADS
    status = catch22_compute(y, n, catch24, mask_nans, out, masked);
    Py_END_ALLOW_THREADS
    free(y);

    const int nOut = catch22_n_features(catch24);
    PyObject * values = PyList_New(nOut);
    PyObject * isMasked = PyList_New(nOut);
    if (values == NULL || isMasked == NULL){
        Py_XDECREF(values);
        Py_XDECREF(isMasked);
        return NULL;
    }
    for (int i = 0; i < nOut; i++) {
        PyList_SET_ITEM(values, i, PyFloat_FromDouble(out[i]));
        PyList_SET_ITEM(isMasked, i, PyBool_FromLong(masked[i]));
    }
    return Py_BuildValue("(NNO)", values, isMasked, status == CATCH22_OK ? Py_True : Py_False);
}

// compute_feature(data, index, mask_nans) -> (value, masked, ok)
static PyObject * compute_feature_wrapper(PyObject * self, PyObject * args)
{
    PyObject * py_input;
    int index;
    int mask_nans = 1;
    if (!PyArg_ParseTuple(args, "Oi|p", &py_input, &index, &mask_nans)){
        return NULL;
    }
    if (index < 0 || index >= CATCH24_N_FEATURES){
        PyErr_SetString(PyExc_IndexError, "feature index out of range");
        return NULL;
    }

    int n;
    double * y = parse_series(py_input, &n);
    if (y == NULL){
        return NULL;
    }

    double out;
    int masked;
    int status;
    Py_BEGIN_ALLOW_THREADS
    status = catch22_compute_feature(y, n, index, mask_nans, &out, &masked);
    Py_END_ALLOW_THREADS
    free(y);

    return Py_BuildValue("(NOO)", PyFloat_FromDouble(out), masked ? Py_True : Py_False,
                         status == CATCH22_OK ? Py_True : Py_False);
}

// features(catch24) -> list of (name, short name, legacy name, hctsa call)
static PyObject * features_wrapper(PyObject * self, PyObject * args)
{
    int catch24 = 0;
    if (!PyArg_ParseTuple(args, "|p", &catch24)){
        return NULL;
    }

    const int nOut = catch22_n_features(catch24);
    PyObject * out = PyList_New(nOut);
    if (out == NULL){
        return NULL;
    }
    for (int i = 0; i < nOut; i++) {
        PyObject * row = Py_BuildValue("(ssss)", catch22_feature_name(i), catch22_short_name(i),
                                       catch22_legacy_name(i), catch22_hctsa_call(i));
        if (row == NULL){
            Py_DECREF(out);
            return NULL;
        }
        PyList_SET_ITEM(out, i, row);
    }
    return out;
}

static PyMethodDef catch22Methods[] = {
    { "compute", compute_wrapper, METH_VARARGS,
      "compute(data, catch24=False, mask_nans=True) -> (values, masked, ok): catch22_compute() on a sequence of numbers" },
    { "compute_feature", compute_feature_wrapper, METH_VARARGS,
      "compute_feature(data, index, mask_nans=True) -> (value, masked, ok): catch22_compute_feature() on a sequence of numbers" },
    { "features", features_wrapper, METH_VARARGS,
      "features(catch24=False) -> list of (name, short name, legacy name, hctsa call)" },
    { NULL, NULL, 0, NULL }
};

static struct PyModuleDef catch22_Cmodule = {
    PyModuleDef_HEAD_INIT,
    "catch22_C",
    "catch22: CAnonical Time-series CHaracteristics (C extension)",
    -1,
    catch22Methods,
};

PyMODINIT_FUNC PyInit_catch22_C(void)
{
    return PyModule_Create(&catch22_Cmodule);
}
