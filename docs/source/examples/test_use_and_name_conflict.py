from pych.extern import Chapel
import os.path

currentloc = os.path.dirname(os.path.realpath(__file__))

@Chapel(module_dirs=[os.path.join(currentloc + '/sfiles/chapel/')], sfile='user.chpl')
def useArbitrary():
    return None

@Chapel(sfile='nonuser.chpl')
def foo(x=int, y=int):
    return int

if __name__ == '__main__':
    useArbitrary()
    print (foo(1, 2)) # Should NOT be 6, should be 2
    # a function called foo from a different source file is used by useArbitrary
    # but that shouldn't interfere with the foo referenced here.

import testcase
# contains the general testing method, which allows us to gather output

def test_using_other_chapel_code():
    """
    ensures that the definition of a function which uses a module containing a
    function named "foo" will not cause the definition of a extern function by
    the same name.
    """
    out = testcase.runpy(os.path.realpath(__file__))
    assert out.endswith('6\n14 14 3 14 14\n14 14 3 14 14\n(contents = 3.0)\n(contents = 3.0)\n2\n')
