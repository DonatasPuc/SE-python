#include <Python.h>

// Function to find gcd in C
int gcd(int a, int b) {
    a = abs(a);
    b = abs(b);

    if (b == 0)
        return a;
    return gcd(b, a % b);
}

// Python wrapper for the C function
static PyObject* py_gcd(PyObject* self, PyObject* args) {
    int a, b, result;

    if (!PyArg_ParseTuple(args, "ii", &a, &b)) {
        PyErr_SetString(PyExc_TypeError, "parameters must be integers");
        return NULL;
    }

    if (a == 0 && b == 0) {
        PyErr_SetString(PyExc_ValueError, "gcd of two zeros is undefined");
        return NULL;
    }

    result = gcd(a, b);

    return PyLong_FromLong(result);
}

// Method table mapping function names to our functions
static PyMethodDef GcdMethods[] = {
    {"gcd", py_gcd, METH_VARARGS, "Calculate the gcd of two numbers"},
    {NULL, NULL, 0, NULL}
};

// Module definition
static struct PyModuleDef gcdmodule = {
    PyModuleDef_HEAD_INIT,
    "gcd_module", /* name of module */
    NULL, /* module documentation */
    -1,
    GcdMethods
};

// Module initialization function
PyMODINIT_FUNC PyInit_gcd_module(void) {
    return PyModule_Create(&gcdmodule);
}