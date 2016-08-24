from __future__ import print_function
from pych.extern import Chapel

@Chapel(sfile='plain.file1.chpl')
def function1():
    return int

@Chapel(sfile='plain.file2.chpl')
def function2():
    return int

if __name__ == '__main__':
    print(function1())
    print(function2())

import testcase
# contains the general testing method, which allows us to gather output

def test_multiple_sfiles():
    assert function1() == 7
    assert function2() == 14
