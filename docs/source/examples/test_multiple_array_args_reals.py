#!/usr/bin/env python
import numpy as np

from pych.extern import Chapel

@Chapel()
def printArray(arr=np.ndarray, arr2 = np.ndarray):
    """
    var arrCopy = arr+arr2;
    writeln(arrCopy);
    """
    return None

if __name__ == "__main__":
    arr = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])
    arr2 = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])
    print arr
    print arr2
    printArray(arr, arr2);

import testcase
# contains the general testing method, which allows us to gather output
import os.path

def test_multiple_array_args_reals():
    out = testcase.runpy(os.path.realpath(__file__))
    # The first time this test is run, it may contain output notifying that
    # a temporary file has been created. The important part is that this
    # expected output follows it (enabling the test to work for all runs, as
    # the temporary file message won't occur in the second run) But that means
    # we can't use ==
    assert out.endswith("2.0 4.0 6.0 8.0 10.0 12.0 14.0 16.0 18.0 20.0\n");
