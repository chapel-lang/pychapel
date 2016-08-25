from builtins import str
from builtins import range
from pych.extern import Chapel

@Chapel()
def ex_for(start=int, end=int):
    """
    for i in start..end {
        writeln("This is ", i);
    }
    return 0.0;
    """
    return float

if __name__ == '__main__':
    ex_for(1, 1000)


import testcase
# contains the general testing method, which allows us to gather output
import os.path

def test_for():
    output = testcase.runpy(os.path.realpath(__file__));
    for i in range(1, 1001):
        assert 'This is ' + str(i) + '\n' in output
