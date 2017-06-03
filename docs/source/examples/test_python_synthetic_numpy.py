#!/usr/bin/env python
from __future__ import print_function
from __future__ import division
from builtins import range
from past.utils import old_div
import argparse
import numpy as np

def simulation(tsteps, spin, decay, velocity):
    """Simulation of some physical phenomenon on a dataset."""

    delta = velocity
    for _ in range(0, tsteps):
        delta = old_div((spin * decay + velocity), delta)

    return np.add.reduce(delta)

def main(tsteps, particles):
    """Load data, run simulation, visualize results."""

    spin = np.ones(particles)               # Load data
    decay = np.ones(particles)
    velocity = np.ones(particles)

    res = simulation(                       # Run simulation
        tsteps,
        spin,
        decay,
        velocity
    )
                                            # Visualize result
    print("Phenomenon after %d tsteps = %d." % (tsteps, res))

if __name__ == "__main__":                  # Argument parsing
    parser = argparse.ArgumentParser(
        description='Example illustrating simulation code.'
    )
    parser.add_argument(
        '--tsteps', help="# of tsteps in 'simulation'",
        type=int,
        required=True
    )
    parser.add_argument(
        '--particles', help="# of elements in arrays '",
        type=int,
        required=True
    )
    args = parser.parse_args()

    main(args.tsteps, args.particles)
    # End of program marker for usage_examples.rst

import testcase
# contains the general testing method, which allows us to gather output
import os.path


def test_example():
    out = testcase.runpy(os.path.realpath(__file__) + ' --tsteps 50 --particles 50000000')
    # The first time this test is run, it may contain output notifying that
    # a temporary file has been created. The important part is that this
    # expected output follows it (enabling the test to work for all runs, as
    # the temporary file message won't occur in the second run) But that means
    # we can't use ==
    assert out.endswith('Phenomenon after 50 tsteps = 50000000.\n')

def test_example49():
    out = testcase.runpy(os.path.realpath(__file__) + ' --tsteps 49 --particles 50000000')
    # The first time this test is run, it may contain output notifying that
    # a temporary file has been created. The important part is that this
    # expected output follows it (enabling the test to work for all runs, as
    # the temporary file message won't occur in the second run) But that means
    # we can't use ==
    assert out.endswith('Phenomenon after 49 tsteps = 100000000.\n')

def test_example51():
    out = testcase.runpy(os.path.realpath(__file__) + ' --tsteps 51 --particles 50000000')
    # The first time this test is run, it may contain output notifying that
    # a temporary file has been created. The important part is that this
    # expected output follows it (enabling the test to work for all runs, as
    # the temporary file message won't occur in the second run) But that means
    # we can't use ==
    assert out.endswith('Phenomenon after 51 tsteps = 100000000.\n')

def test_example48():
    out = testcase.runpy(os.path.realpath(__file__) + ' --tsteps 48 --particles 50000000')
    # The first time this test is run, it may contain output notifying that
    # a temporary file has been created. The important part is that this
    # expected output follows it (enabling the test to work for all runs, as
    # the temporary file message won't occur in the second run) But that means
    # we can't use ==
    assert out.endswith('Phenomenon after 48 tsteps = 50000000.\n')

def test_example52():
    out = testcase.runpy(os.path.realpath(__file__) + ' --tsteps 52 --particles 50000000')
    # The first time this test is run, it may contain output notifying that
    # a temporary file has been created. The important part is that this
    # expected output follows it (enabling the test to work for all runs, as
    # the temporary file message won't occur in the second run) But that means
    # we can't use ==
    assert out.endswith('Phenomenon after 52 tsteps = 50000000.\n')
