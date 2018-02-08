# Copyright 2014-2018 Cray Inc.
# Other additional copyright holders may be indicated within.
#
# The entirety of this work is licensed under the Apache License,
# Version 2.0 (the "License"); you may not use this file except
# in compliance with the License.
#
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
