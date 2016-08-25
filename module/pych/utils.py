"""
Utility functions used across modules.
"""
from __future__ import print_function
import os

def prepend_path(root, path):
    """
    Prefix 'path' with 'root' when 'path is not an absolute path.

    :param root str: String to prepend to path.
    :param path str: The path that will be prefixes with 'root'.
    """

    abspath = path
    if not os.path.isabs(abspath):
        abspath = "%s%s%s" % (root, os.sep, path)
    abspath = os.path.abspath(abspath)

    return abspath

#
# Helper functions for printing output form the pych command
# we do not want to use the logging module since that would
# mess with the configured output of the pych module.
#
def info(msg):
    """
    Print out a information message...
    :param msg str: The message to print.
    """
    print(msg)

def warn(msg):
    """
    Print out a warning message...
    :param msg str: The warning message to print.
    """
    print("WARN: %s" % msg)

def error(msg):
    """
    Print out an error message...
    :param msg str: The error message to print.
    """
    print("ERR: %s" % msg)
