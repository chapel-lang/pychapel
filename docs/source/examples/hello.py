from __future__ import print_function
import logging

import pych
from pych.extern import FromC

#
# Mapping the Python function "hello_cworld" to the
# C-function "hello_world".
#
@FromC(clib="libexamples.so", ename="hello_world")
def hello_cworld():
    return None

#
# Mapping the Python function "add_ints" to the
# C-function "add_ints".
#
@FromC(clib="libexamples.so", ename="add_ints")
def add_ints(x=int, y=int):
    return int

#
# Mapping the Python function "add_doubles" to the
# C-function "add_doubles".
#
@FromC(clib="libexamples.so", ename="add_doubles")
def add_doubles(x=float, y=float):
    return float

#@FromC()
#def add(x, y):
#    """
#    return x+y;
#    """
#    return int

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    print(hello_cworld())
    print(add_ints(1, 2))
    print(add_doubles(1.0, 2.0))
    print(add_doubles(1.0, 2.0))
    print(add_doubles(1.0, 2.0))
