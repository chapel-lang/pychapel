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
    Responsible for opening libraries, loading functions and maintaining
    handles to both.
"""
from builtins import object
from ctypes import cdll
import ctypes
import operator
import logging
import pprint
import glob
import os

from pych.exceptions import LibraryError
from pych.utils import prepend_path

class ObjectStore(object):
    """The object cache encapsulation."""

    def __init__(self, config):

        self._search_paths = config["search_paths"]
        self._output_paths = config["output_paths"]

        self._functions = {}
        self._libraries = {}                # library.so => cdll-library-handle

        self._initializers = {}             # Chapel RT initializers
        self._finalizers = {}               # Chapel RT finalizers
        logging.debug("Object-store: %s", self)

    def __del__(self):
        for lib in self._finalizers:
            self._finalizers[lib]()

    def __repr__(self):
        return pprint.pformat(vars(self))

    def open(self, library_abspath):
        """
        Open a library, store a handle to it and return the handle.

        :param str library_abspath: Absolute path to the library (.so).
        :returns: Handle to library when successful, None othervise.
        :rtype: ctypes.CDLL

        :raises OSError: When 'library_abspath' is not found.
        """
        library_fn = os.path.basename(library_abspath)
        if library_fn not in self._libraries:   # Avoid reopening libraries
            self._libraries[library_fn] = cdll.LoadLibrary(library_abspath)

        return self._libraries[library_fn]

    def open_ahead(self):
        """Open handles to all libraries in search paths."""

        for search_path in self._search_paths:
            for library_abspath in glob.glob("%s/*.so" % search_path):
                self.open(library_abspath)

    def open_fn(self, library_fn):
        """
        Look through the search_paths for 'library_fn', opening the first
        matching library via open(...) thereby implicitly also storing a handle
        to it.

        :param str library_fn: Filename of library without path, eg. "libc.so".
        :returns: Handle to library when successful, None othervise.
        :rtype: ctypes.CDLL
        """
        for source in self._search_paths:
            for search_path in self._search_paths[source]:
                library_abspath = "%s/%s" % (search_path, library_fn)
                if os.path.exists(library_abspath):
                    return self.open(library_abspath)

        return None

    def load(self, library_fn, function_name):
        """
        Load a function from library, store a handle to it, and return
        the handle.

        :param str library_fn: Filename of library without path, eg. "libc.so".
        :param str function_name: Name of the function, eg. "printf".
        :returns: Handle to library function as a ctypes function pointer.
        :rtype: ctypes._FuncPtr
        :raises AttributeError: When function is not in library.
        """

        handle = operator.attrgetter(function_name)(self._libraries[library_fn])

        self._functions[function_name] = handle

        return self._functions[function_name]


    def evoke(self, extern):
        """Evoke the efunc related the given Extern,
        channeling all the power of the mighty ObjectStore.

        This entails going through the "hierachy":

        1. Check and see if function pointer is readily available.
        2. Try loading from existing library handle.
        3. Search for library associated with 'extern', open library, and load
           function.

        Hitting 3) should only occur the first time an Extern is evoked.

        Meaning that evocations of different Externs in the same library
        will not go to disk.

        Similarly, multiple evocations of the same Extern will only result in a
        lookup.

        :param pych.Extern extern: External to conjure up a materialization.

        :rtype: ctypes._FuncPtr
        :returns: Handle to library function as a ctypes function pointer.
        """

        if extern.ename in self._functions:     # Grabbing loaded symbols
            return self._functions[extern.ename]

        try:    # Loading it from associated library aka dlload()...
            return self.load(extern.lib, extern.ename)
        except KeyError:
            logging.debug("No library-handle for: [%s]", extern.lib)
        except AttributeError:
            logging.error(
                "Library(%s) found but ename(%s) is not in it.",
                extern.lib,
                extern.ename
            )

        try:    # Opening library from disk and loading aka dlopen(), dlload()
            lib_h = self.open_fn(extern.lib)
            if lib_h:
                # Initialize the Chapel runtime if it is a Chapel library
                if extern.slang.lower() == "chapel":
                    initializer = self.load(extern.lib, "chpl_library_init")
                    finalizer = self.load(extern.lib, "chpl_library_finalize")

                    initializer.argtypes = [
                        ctypes.c_int,
                        ctypes.POINTER(ctypes.c_char_p)
                    ]
                    initializer(
                        1,
                        ctypes.c_char_p("chapel_library")
                    )
                    self._initializers[extern.lib] = initializer
                    self._finalizers[extern.lib] = finalizer

                return self.load(extern.lib, extern.ename)
        except AttributeError as exc:
            raise LibraryError(extern, cause=exc)

        logging.debug(
            "I used all my magic but failed evoking the ufunc for extern."
        )
        return None                                     # At last we give up
