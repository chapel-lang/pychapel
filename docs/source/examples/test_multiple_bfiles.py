from __future__ import print_function
from pych.extern import Chapel

@Chapel(bfile='file1.plain.chpl')
def functionA():
    return int

@Chapel(bfile='file2.plain.chpl')
def functionB():
    return int

if __name__ == '__main__':
    print(functionA())
    print(functionB())

import testcase
# contains the general testing method, which allows us to gather output

def test_multiple_bfiles():
    assert functionA() == 8
    assert functionB() == 16
