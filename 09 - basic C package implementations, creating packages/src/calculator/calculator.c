#define PY_SSIZE_T_CLEAN
#include <Python.h>

static PyObject* add(PyObject* self, PyObject* args) {
    double a, b;
    if (!PyArg_ParseTuple(args, "dd", &a, &b)) {
        PyErr_SetString(PyExc_TypeError, "Arguments must be numbers (int or float)");
        return NULL;
    }
    return PyFloat_FromDouble(a + b);
}

static PyObject* sub(PyObject* self, PyObject* args) {
    double a, b;
    if (!PyArg_ParseTuple(args, "dd", &a, &b)) {
        PyErr_SetString(PyExc_TypeError, "Arguments must be numbers (int or float)");
        return NULL;
    }
    return PyFloat_FromDouble(a - b);
}

static PyObject* mul(PyObject* self, PyObject* args) {
    double a, b;
    if (!PyArg_ParseTuple(args, "dd", &a, &b)) {
        PyErr_SetString(PyExc_TypeError, "Arguments must be numbers (int or float)");
        return NULL;
    }
    return PyFloat_FromDouble(a * b);
}

static PyObject* div_(PyObject* self, PyObject* args) {
    double a, b;
    if (!PyArg_ParseTuple(args, "dd", &a, &b)) {
        PyErr_SetString(PyExc_TypeError, "Arguments must be numbers (int or float)");
        return NULL;
    }
    if (b == 0) {
        PyErr_SetString(PyExc_ZeroDivisionError, "division by zero");
        return NULL;
    }
    return PyFloat_FromDouble(a / b);
}

static PyMethodDef CalculatorMethods[] = {
    {"add", add, METH_VARARGS, "Add two numbers"},
    {"sub", sub, METH_VARARGS, "Subtract two numbers"},
    {"mul", mul, METH_VARARGS, "Multiply two numbers"},
    {"div", div_, METH_VARARGS, "Divide two numbers"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef calculatormodule = {
    PyModuleDef_HEAD_INIT,
    "calculator",
    NULL,
    -1,
    CalculatorMethods
};

PyMODINIT_FUNC PyInit_calculator(void) {
    return PyModule_Create(&calculatormodule);
}
