import logging

import pych
from pych.extern import FromC

#
# Mapping the Python function "hello_cworld" to the
# C-function "hello_c".
#
@FromC(clib="libexamples.so", cname="hello_world")
def hello_cworld():
    return None

#
# Mapping the Python function "" to the
# C-function "hello_c".
#
@FromC(clib="libexamples.so", cname="add_ints")
def add_ints(x, y):
    return int

#
# Mapping the Python function "" to the
# C-function "hello_c".
#
@FromC(clib="libexamples.so", cname="add_doubles")
def add_doubles(x, y):
    return float

#@FromC()
#def add(x, y):
#    """
#    return x+y;
#    """
#    return int

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    print hello_cworld()

    print add_ints(1, 2)
    print add_floats(1.0, 2.0)
