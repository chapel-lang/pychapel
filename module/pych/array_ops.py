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
Explicit mapping of NumPy array operations to Chapel array operations.
"""
from pych.extern import Chapel
import numpy as np
# pylint: disable=no-member
# The ndarray member is added dynamically and therefore not visible to pylint.
# pylint: disable=unused-argument
# The interoperability interface exploits arguments, their use are therefore
# not visible to pylint.

@Chapel()
def pych_ewise_add(in1=np.ndarray, in2=np.ndarray, res=np.ndarray):
    """
    res = in1 + in2;
    """
    return None

#@Chapel()
#def pych_ewise_assign(in1=np.ndarray, res=np.ndarray):
#    """
#    res = in1;
#    """

@Chapel()
def pych_ewise_assign(in1=int, res=np.ndarray):
    """
    res = in1;
    """
    return None

@Chapel()
def pych_ewise_subtract(in1=np.ndarray, in2=np.ndarray, res=np.ndarray):
    """
    res = in1 - in2;
    """
    return None

@Chapel()
def pych_scan_add(in1=np.ndarray, in2=np.ndarray, res=np.ndarray):
    """
    res = in1 - in2;
    """
    return None

@Chapel()
def pych_reduce_add(in1=np.ndarray, axis=int, res=np.ndarray):
    """
    res = +reduce(in1);
    """
    return None

