from __future__ import print_function
from pych.extern import Chapel
import os.path

currentloc = os.path.dirname(os.path.realpath(__file__))

@Chapel(module_dirs=[os.path.join(currentloc + '/multMods1/'), os.path.join(currentloc + '/multMods2/')], sfile="users.multiple.chpl")
def useMultiModules(x=int, y=int):
    return int

if __name__ == "__main__":
    print(useMultiModules(2, 4))

def test_using_multiple_modules():
    """
    tests that specifying multiple directories with the decorator argument
    "module_dirs" works.
    """
    assert useMultiModules(2, 4) == 28
