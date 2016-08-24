"""
    The "Runtime", the top of the organization.

    Sets up object_store, specializer, compilers in to
    orchestrate materialization of Externs and initialization
    of Externs/libraries.
"""
from builtins import object
import logging
import ctypes

from pych.types import PychArray
from pych.object_store import ObjectStore
from pych.specializer import get_specializer
from pych.compiler import Compiler
from pych.exceptions import MaterializationError, CompilationError

class Runtime(object):
    """Encapsulation of runtime activities, compilation, loading, etc."""

    def __init__(self, config):
        """
        :param config pych.Config: pyChapel configuration
        """

        self.hints = {}                 # Decorator hints are stored here
        self.arrays = {}                # Array mappings
        self.compilers = {}             # Backend compilers
        self.specializers = {}          # Sourcecode generators/specializers

        self.object_store = ObjectStore(        # Init object-store
            config["object_store"]
        )
        if config["open_ahead"]:
            self.object_store.open_ahead()

        for compiler in config["compilers"]:    # Init compilers
            self.compilers[compiler] = Compiler(
                config["compilers"][compiler]
            )

        for slang in config["specializers"]["templates"]:   # Init specializers
            self.specializers[slang] = get_specializer(slang)(
                config["specializers"]["templates"][slang],
                config["specializers"]["sfiles"][slang],
                config["specializers"]["bfiles"][slang]
            )

    def hint(self, extern):
        """
        Hint the runtime that we might be interested in this extern
        at some point in the future.
        """
        if extern.lib not in self.hints:
            self.hints[extern.lib] = []

        self.hints[extern.lib].append(extern)

    def materialize(self, extern):
        """
        Materializes an extern.

        That means doing all it can to obtain a ctypes._FuncPtr that usable as
        the "efunc" attribute of the given Extern:

        - Compile it using an inline-template
        - Compile it from a sourcefile
        - Compile it using a specialization template

        Or "Just" load it if defined as a library-wrapper
         and possibly other stunts.

        The first time code is compiled/materialized is
        For dynamically compiled code from either inline or source,
        materialization needs to determine if the source has changed.

        It is up to the caller to check the return-value of the function.
        Meaning the caller must/should check whether or not it was possible
        to materialize the Extern.

        :param pych.Extern extern: The Extern to "materialize".
        :returns: A ctypes function pointer when successful, None othervise.
        :rtype: ctypes._FuncPtr

        :assumes:   That the caller has checked that the Extern
                    is not yet materialized aka verified that
                    Extern.efunc == None.
                    Nothing bad will happen except for unnessecary work.

        :contracts: Materialization should not occur until after all
                    mapped functions have been decorated. This limitation
                    should be removed somehow... some day...
        """

        efunc = self.object_store.evoke(extern) # Evoke the efunc

        if not efunc:                           # Create an evokeable object
            source = ""
            slang = extern.slang.lower() if extern.slang else None

            if (extern.doc or extern.sfile) and \
                slang not in ["c", "chapel"]:
                raise MaterializationError(
                    extern,
                    "Unsupported source language(%s)" % extern.slang
                )

            if extern.doc:                      # Specialize inline
                # Use hints to specialize source for all externs
                # mapped into this library
                source = self.specializers[slang].specialize(
                    self.hints[extern.lib]
                )

            if extern.sfile:
                # TODO: Wrap exported externs to ensure correct argument
                # conversion
                source = self.specializers[slang].load(
                    extern.sfile
                )

            if source:                          # Compile the source
                out = err = ""
                chplflags = ''
                if extern.module_dirs:
                    # Assumes module_dirs field only used by Chapel extern
                    chplflags = ' '.join(['-M '+elt for elt in extern.module_dirs])
                try:
                    out, err = self.compilers[slang].compile(
                        source, slang, "%s/%s" % (
                            self.object_store._output_paths[slang],
                            extern.lib
                        ), chplflags
                    )
                except CompilationError as exc:
                    raise MaterializationError(
                        extern,
                        " due to compilation error",
                        exc
                    )
                    
                if out:
                    logging.info("Compiler said something: %s", out)
                if err:
                    logging.error("Compiler complained: %s", err)

                efunc = self.object_store.evoke(extern) # Evoke it again!

        return efunc

    def map_nparray(self, nparray):
        """
        Map a NumPy array to a PychArray for ctypes interoperability.

        :param numpy.ndarray nparray: The NumPy array to map
        :returns: A PychArray usable by ctypes
        :rtype: pych.PychArray
        """
        nparray_id = id(nparray)

        try:
            return self.arrays[nparray_id]
        except KeyError:
            logging.debug("Array is not mapped... yet...")

        #
        # Create one
        #
        shape = [nelements for nelements in nparray.shape]
        shape += [0]*(16-len(shape))

        strides = [stride for stride in nparray.strides]
        strides += [0]*(16-len(strides))
        logging.debug(
            "Mapping array[%d] data=%d",
            nparray_id,
            nparray.ctypes.data
        )
        self.arrays[nparray_id] = PychArray(
            two=2,
            nd=nparray.ndim,
            typekind=nparray.__array_interface__['typestr'][1],
            itemsize=nparray.itemsize,
            flags=0,
            shape=(ctypes.c_int*16)(*shape),
            strides=(ctypes.c_int*16)(*strides),
            ptr_d=nparray.ctypes.data,
            ident=nparray_id
        )

        return self.arrays[nparray_id]
