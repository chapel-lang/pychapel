from builtins import str
from builtins import range
from pych.extern import Chapel

@Chapel(sfile="forall.exported.chpl")
def ex_forall(start=int, end=int):
    return float

if __name__ == "__main__":
    ex_forall(1, 10000)

import testcase
# contains the general testing method, which allows us to gather output
import os.path

def test_forall():
    output = testcase.runpy(os.path.realpath(__file__))
    for i in range(1, 10001):
        assert 'This is ' + str(i) + '\n' in output
