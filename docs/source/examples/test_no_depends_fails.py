from __future__ import print_function
from pych.extern import Chapel

@Chapel(sfile="users.onlyonce.chpl")
def useTwoModules(x=int, y=int):
    return int

if __name__ == "__main__":
    print(useTwoModules(2, 4))

import testcase
# contains the general testing method, which allows us to gather output
import os.path

def test_using_multiple_modules():
    out = testcase.runpy(os.path.realpath(__file__))
    # Ensure that when a used module is nowhere near the exported function, we
    # get an error message to that effect.
    assert "error: Cannot find module or enum" in out
