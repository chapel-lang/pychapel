#!/usr/bin/env python
from __future__ import print_function
import ctypes

def main():
    chpl = ctypes.cdll.LoadLibrary("chapel.so")
    chpl.chpl_library_init.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_char_p)] 
    argv=(ctypes.c_char_p*1)()
    argv[0] = "chapel"
    chpl.chpl_library_init(0, argv)

    print(chpl.nicestuff(1000, 1000, 20))

    chpl.chpl_library_finalize()
    return chpl

if __name__ == "__main__":
    main()
