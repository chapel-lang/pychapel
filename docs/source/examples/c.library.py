from __future__ import print_function
from pych.extern import Extern

#
# Mapping the Python function "hello_world" to the function "hello_world"
# from the library "libexamples.so".
#
@Extern(lib="libexamples.so", ename="hello_world")
def hello_world():
    return None

#
# Mapping the Python function "add_ints" to the function "add_ints"
# from the library "libexamples.so".
#
@Extern(lib="libexamples.so", ename="add_ints")
def add_ints(x=int, y=int):
    return int

#
# Mapping the Python function "add_doubles" to the function "add_doubles"
# from the library "libexamples.so".
#
@Extern(lib="libexamples.so", ename="add_doubles")
def add_doubles(x=float, y=float):
    return float

if __name__ == "__main__":
    print(hello_world())
    print(add_ints(1, 2))
    print(add_doubles(1.0, 2.0))
