#include <Python.h>

int main()
{
    Py_Initialize();

    // Load the python module
    PyObject* pName = PyUnicode_DecodeFSDefault("rational");
    PyObject* pModule = PyImport_Import(pName);
    Py_DECREF(pName);

    if (pModule != NULL) {
        // Get the RationalNumber class
        PyObject* pClass = PyObject_GetAttrString(pModule, "RationalNumber");

        // Arguments for the RationalNumber instances
        PyObject* pArgs1 = PyTuple_Pack(2, PyLong_FromLong(6), PyLong_FromLong(8));
        PyObject* pArgs2 = PyTuple_Pack(2, PyLong_FromLong(3), PyLong_FromLong(4));

        // Create two RationalNumber instances
        PyObject* pInstance1 = PyObject_CallObject(pClass, pArgs1);
        PyObject* pInstance2 = PyObject_CallObject(pClass, pArgs2);

        // Multiply the two instances
        PyObject* result = PyObject_CallMethod(pInstance1, "__mul__", "O", pInstance2);

        // Print the result
        PyObject* resultStr = PyObject_Repr(result);
        printf("Result: %s\n", PyUnicode_AsUTF8(resultStr));

        // Cleanup
        Py_DECREF(pArgs1);
        Py_DECREF(pArgs2);
        Py_DECREF(pInstance1);
        Py_DECREF(pInstance2);
        Py_DECREF(result);
        Py_DECREF(resultStr);
    }
    else {
        PyErr_Print();
    }

    Py_DECREF(pModule);
    Py_Finalize();

    return 0;
}