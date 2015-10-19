from pych.extern import Chapel
import os.path

currentloc = os.path.dirname(os.path.realpath(__file__))

@Chapel(module_dirs=[os.path.join(currentloc + '/bfiles/chapel/')], bfile="bfile.user.chpl")
def useArbitraryBfile():
    return None


if __name__ == "__main__":
    useArbitraryBfile()

import testcase
# contains the general testing method, which allows us to gather output

def test_using_other_chapel_code():
    """
    ensures that a bfile definition of a Chapel function with a use statement
    will work when the module being used lives in a directory specified with
    the decorator argument "module_dirs"
    """
    out = testcase.runpy(os.path.realpath(__file__))
    assert out.endswith('6\n14 14 3 14 14\n14 14 3 14 14\n(contents = 3.0)\n(contents = 3.0)\n')
