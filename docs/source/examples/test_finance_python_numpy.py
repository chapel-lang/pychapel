#!/usr/bin/env python
from __future__ import print_function
import argparse
import time

import matplotlib
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import numpy as np

elapsed = [time.time()]

def measure(text=""):
    """Measure execution time."""

    global elapsed
    elapsed.append(time.time())
    if text:
        text += " "
        print("%s%f" % (text, elapsed[-1] - elapsed[-2]))

def visualize(date, bid, ask, voodoo, spread=30):
    """Plot bid price, asking price and "voodoo" values."""

    # Downsample
    dateDs, bidDs, askDs, voodooDs = (
        date[::spread], bid[::spread], ask[::spread], voodoo[::spread]
    )

    fig = plt.figure(figsize=(10,7))
    ax1 = plt.subplot2grid((40,40), (0,0), rowspan=40, colspan=40)

    ax1.plot(date, bid)
    ax1.plot(date, ask)
    plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)

    ax1_2 = ax1.twinx()
    ax1_2.fill_between(date, 0, voodoo, facecolor='g', alpha=.3)

    plt.subplots_adjust(bottom=.23) 
    plt.grid(True)
    plt.show()
    plt.close()

def load_prices(filename):
    """Load stock-prices."""

    date, bid, ask = np.loadtxt(
        filename,
        unpack=True,
        delimiter=',',
    )
    voodoo = np.empty(date.shape)

    return date, bid, ask, voodoo

def quant(date, bid, ask, voodoo):
    """Apply some financial voodoo."""

    future = 200
    voodoo[:] = ask-bid
    for i in xrange(0, future):
        voodoo += (ask-bid + ask-bid  + ask-bid + ask-bid
                   +ask-bid + ask-bid + ask-bid + ask-bid
                  ) / 8
    voodoo[:] = voodoo / future

def main(filename, with_viz=True):
    date, bid, ask, voodoo = load_prices(filename)      # Load dataset
    measure()
    quant(date, bid, ask, voodoo)                       # Compute something
    measure("Computation took")
    
    if with_viz:
        visualize(date, bid, ask, voodoo)               # Visualize the results

    return voodoo

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Example illustrating a synthetic finance code.'
    )
    parser.add_argument(
        '--filename', help="Path to filename", type=str, required=True
    )
    parser.add_argument(
        '--no-viz', help="Disable visualization", action='store_true'
    )
    args = parser.parse_args()
    R = main(args.filename, not args.no_viz)
    print(R.sum())

import testcase
# contains the general testing method, which allows us to gather output
import os

def test_example():
    filename = os.sep.join([
        os.path.dirname(os.path.realpath(__file__)), "aux", "GBPUSD1m.txt"
    ])
    out = testcase.runpy(
        os.path.realpath(__file__) + ' --filename %s --no-viz' % filename
    )
    assert out.endswith('171.26344695\n')
