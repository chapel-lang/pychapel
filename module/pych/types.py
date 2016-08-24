"""
    Mapping of types between Python - NumPy - ctypes.
"""
# pylint: disable=no-member
# The ndarray member is added dynamically and therefore not visible to pylint.
# pylint: disable=too-few-public-methods
# The classes here are ctypes structures, it is therefore completely valid
# that they have few public methods.

import ctypes
import numpy as np

class PychArray(ctypes.Structure):
    """
    Representation of a NumPy array when interoperating with C/Chapel
    via ctypes.
    """

    _fields_ = [
        ('two', ctypes.c_int),
        ('nd', ctypes.c_int),
        ('typekind', ctypes.c_char),
        ('itemsize', ctypes.c_int),
        ('flags', ctypes.c_int),
        ('shape', ctypes.c_int*16),
        ('strides', ctypes.c_int*16),
        ('ptr_d', ctypes.c_void_p),
        ('ident', ctypes.c_int)
    ]

TYPEMAP = {
    None:       None,
    bool:       ctypes.c_bool,
    int:        ctypes.c_int,
    int:       ctypes.c_long,
    float:      ctypes.c_double,
    str:        ctypes.c_char_p,
    str:    ctypes.c_wchar_p,
    np.ndarray: ctypes.POINTER(PychArray)
}

TYPE2SOURCE = {
    "c": {
        None:       "void",
        bool:       "bool",
        int:        "int",
        int:       "long",
        float:      "double",
        str:        "char*",
        str:    "char*",
        np.ndarray: "pych_array*"
    },
    "chapel": {
        None:       "void",
        bool:       "bool",
        int:        "int",
        int:       "int(64)",
        float:      "real(64)",
        str:        "string",
        str:    "string",
        np.ndarray: "pych_array"
    }
}

CHPL2PY = {
    None:       "None",
    "bool":     "bool",
    "int":      "int",
    "int(16)":  "int",
    "int(32)":  "int",
    "int(64)":  "int",
    "real":     "float",
    "real(32)": "float",
    "real(64)": "float"
}

KEYWORDS = {
    "c": [],
    "chapel": [
        "_", "align", "atomic", "begin", "break", "by", "class", "cobegin",
        "coforall", "config", "const", "continue", "delete dmapped", "do",
        "domain", "else", "enum", "export", "extern", "for", "forall", "if",
        "in", "index inline", "inout", "iter", "label", "let", "local",
        "module", "new", "nil", "noinit", "on", "otherwise out", "param",
        "proc", "record", "reduce", "ref", "return", "scan", "select",
        "serial", "single", "sparse subdomain", "sync", "then", "type",
        "union", "use", "var", "when", "where", "while", "yield", "zip"
    ]
}
