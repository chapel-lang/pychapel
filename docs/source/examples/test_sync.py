from builtins import str
from builtins import range
from pych.extern import Chapel

@Chapel()
def ex_sync():
    """
    writeln("Starting!");
    sync {
        begin writeln("#1 line.");
        begin writeln("#2 line.");
        begin writeln("#3 line.");
        begin writeln("#4 line.");
        begin writeln("#5 line.");
    }
    writeln("DONE!");
    """
    return None

if __name__ == '__main__':
    ex_sync()

import testcase
# contains the general testing method, which allows us to gather output
import os.path

def test_sync():
    out = testcase.runpy(os.path.realpath(__file__))
    # The first time this test is run, it may contain output notifying that
    # a temporary file has been created.  The important part is that this
    # expected output follows it (enabling the test to work for all runs, as
    # the temporary file message won't occur in the second run)  But that means
    # we can't use out.startswith

    # ensure starts and ends with correct statements
    startLoc = out.find('Starting!\n')
    assert startLoc >= 0
    # ensure contains all of the remainder
    for i in range(1, 6):
        lineLoc = out.find('#' + str(i) + ' line.\n')
        assert lineLoc >= 0
        assert lineLoc >= startLoc
    assert out.endswith('DONE!\n')
