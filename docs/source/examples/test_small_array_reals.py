#!/usr/bin/env python
import numpy as np

from pych.extern import Chapel

@Chapel()
def printArray(arr=np.ndarray):
    """
    writeln(arr);
    """
    return None

if __name__ == "__main__":
    arr = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])
    print arr
    printArray(arr);

import testcase
# contains the general testing method, which allows us to gather output
import os.path

def test_small_array_reals():
    out = testcase.runpy(os.path.realpath(__file__))
    # The first time this test is run, it may contain output notifying that
    # a temporary file has been created. The important part is that this
    # expected output follows it (enabling the test to work for all runs, as
    # the temporary file message won't occur in the second run) But that means
    # we can't use ==
    assert out.endswith("1.0 2.0 3.0 4.0 5.0 6.0 7.0 8.0 9.0 10.0\n");
