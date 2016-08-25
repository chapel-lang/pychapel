from builtins import str
from builtins import range
from pych.extern import Chapel

@Chapel()
def ex_begin_noret():
    """
    writeln("Starting!");
    begin writeln("#1 line.");
    begin writeln("#2 line.");
    begin writeln("#3 line.");
    begin writeln("#4 line.");
    begin writeln("#5 line.");
    """
    return None

@Chapel()
def ex_begin():
    """
    writeln("Starting part2!");
    begin writeln("#6 line.");
    begin writeln("#7 line.");
    begin writeln("#8 line.");
    begin writeln("#9 line.");
    begin writeln("#10 line.");
    return 0;
    """
    return int

if __name__ == '__main__':
    ex_begin_noret()
    ex_begin()

import testcase
# contains the general testing method, which allows us to gather output
import os.path

def test_begin():
    out = testcase.runpy(os.path.realpath(__file__))
    # The first time this test is run, it may contain output notifying that
    # a temporary file has been created.  The important part is that this
    # expected output follows it (enabling the test to work for all runs, as
    # the temporary file message won't occur in the second run)  But that means
    # we can't use out.startswith

    # ensure starts and ends with correct statements
    startLoc = out.find('Starting!\n')
    assert startLoc >= 0
    # While we can't ensure that all of the first function's output has occurred
    # before the second function begins, we can ensure that their starting
    # output is in order
    secondStart = out.find('Starting part2!\n')
    assert secondStart > startLoc
    # ensure contains all of the remainder
    for i in range(1, 11):
        lineLoc = out.find('#' + str(i) + ' line.\n')
        assert lineLoc >= 0
        assert lineLoc >= startLoc
        if (i > 5):
            assert lineLoc > secondStart
