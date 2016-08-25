from __future__ import print_function
from pych.extern import Chapel

@Chapel(sfile="exported.and.not.chpl")
def foo(x=int, y=int):
    return int

if __name__ == '__main__':
    print(foo(3, 5))

import testcase
# contains the general testing method, which allows us to gather output
import os.path

def test_sfile():
    assert foo(3, 5) == -13
