from __future__ import print_function
from pych.extern import Chapel

@Chapel(bfile="bfile.fib.chpl")
def fibonacci(n=int):
    return int

if __name__ == "__main__":
    print(fibonacci(10))

def test_fib():
    assert fibonacci(10) == 55
