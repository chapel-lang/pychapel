"""
    The Specializer is responsible for loading up sourcecode,
    specializing code-templates for Externs and possibly other
    things down the road.
"""
from builtins import str
from builtins import zip
from builtins import object
# pylint: disable=no-member
# The ndarray member is added dynamically and therefore not visible to pylint.

import logging
import os

import numpy as np

from pych.types import TYPE2SOURCE

def get_specializer(slang):
    """
    Return a specializer instance for the given source language (slang).

    :param str slang: Source language, e.g. "c" or "chapel".
    :returns: A specializer for the given source language.
    :rtype: CSpecializer|ChapelSpecializer
    """
    if slang.lower() == "c":
        return CSpecializer
    elif slang.lower() == "chapel":
        return ChapelSpecializer
    elif slang.lower() == "python":
        return PythonSpecializer
    else:
        logging.error("Cannot find specializer for slang(%s).", slang)
        return None

class BaseSpecializer(object):
    """
    Handles loading of source-code and code-templates for specialization.
    The actual language-specific specialization is performed by subclasses.
    """

    def __init__(self, template_paths, sfile_paths, bfile_paths):
        self.templates = template_paths
        self.sfiles = sfile_paths
        self.bfiles = bfile_paths
        self.sources = {}
        self.mtime = {}

    def abs_path(self, filename):
        """
        Constructs the absolute path to 'filename', (if it isn't already).
        This will return a absolute path to 'filename' within one of the
        template or sfile directories.

        :param filename str: Filename to construct abspath for.
        :return: Absolute path to 'filename', None when it can't be found.
        :rtype: str
        """
        path = None
        if os.path.isabs(filename): # Absolute, just use it.
            path = filename
        else:                       # Search for it in sfiles dirs
            basename = os.path.basename(filename)
            for root in self.templates + self.sfiles + self.bfiles:
                candidate = os.sep.join([root, basename])
                if os.path.exists(candidate):
                    path = candidate
                    break

        return path

    def load(self, filename):
        """
        Reads content of 'filename' into sources dict and returns the
        content.

        :param str filename: Filename without path.
        :returns: Filecontents, None if contents cannot be found.
        :rtype: str
        """
        if filename not in self.sources:
            path = self.abs_path(filename)
            if not path:
                raise IOError("Cannot find source for filename(%s)" % filename)

            self.sources[filename] = open(path).read()
            self.mtime[filename] = int(os.stat(path).st_mtime)

        return self.sources[filename]

    def specialize(self, externs, prefix=True):
        """The function performing the actual specialization for the given Extern(s).

        :param pych.Extern externs: List of Externs to specialize.

        :rtype: str
        :returns: Sourcecode in the Externs language.

        :raises NotImplementedError: When using the BaseSpecializer directly.
            Use the "targeted" specializer for C or Chapel.

        """
        raise NotImplementedError("Do not use the BaseSpecializer directly.")

class PythonSpecializer(BaseSpecializer):
    """Specializer for Python modules."""

    def __init__(self, template_paths, sfile_paths, bfile_paths):
        super(PythonSpecializer, self).__init__(
            template_paths,
            sfile_paths,
            bfile_paths
        )

    def specialize(self, externs, prefix=True):
        return ""

class CSpecializer(BaseSpecializer):
    """Specializer for C code."""

    def __init__(self, template_paths, sfile_paths, bfile_paths):
        super(CSpecializer, self).__init__(
            template_paths,
            sfile_paths,
            bfile_paths
        )

    def specialize(self, externs, prefix=True):
        """Specialize the inline-c code-template to the given externs."""

        # Grab the "template"
        source = ""
        if prefix:
            source = self.load("prefix.c")

        tmpl = self.load("func.c")
        for extern in externs:

            # Create the function signature
            args = ["%s %s" % (TYPE2SOURCE["c"][atype], aname)
                for aname, atype in
                zip(extern.anames, extern.atypes)
            ]

            func_text = {
                "rtype":   TYPE2SOURCE["c"][extern.rtype],
                "args":    ", ".join(args),
                "ename":   extern.ename,
                "fbody":   extern.doc
            }
            source += tmpl % func_text

        return source

class ChapelSpecializer(BaseSpecializer):
    """Specializer for Chapel code."""

    def __init__(self, template_paths, sfile_paths, bfile_paths):
        super(ChapelSpecializer, self).__init__(
            template_paths,
            sfile_paths,
            bfile_paths
        )

    def specialize(self, externs, prefix=True):
        """Specialize the inline-chapel code-template to the given externs."""

        # Grab the "template"
        source = ""
        if prefix:
            source = self.load("prefix.chpl")

        for extern in externs:
            # The function that won't get exported
            tmpl_internal = self.load("inline.func.internal.chpl")

            # NumPy conversion
            conv_pych = self.load("convert.pych.1d.chpl")

            # The function that will get exported
            if extern.rtype:
                tmpl = self.load("inline.func.export.return.chpl")
            else:
                tmpl = self.load("inline.func.export.noreturn.chpl")

            #
            # Exported signature
            pars = []
            conversion = ""
            logging.debug("Args: %s", str(extern.anames))
            logging.debug("Atypes: %s", str(extern.atypes))
            for aname, atype in zip(extern.anames, extern.atypes):
                aname_postscript = ""
                if atype is np.ndarray:
                    aname_postscript = "_pych"
                    conversion += conv_pych % {"aname": aname}

                pars.append("%s%s: %s" % (
                    aname, aname_postscript, TYPE2SOURCE["chapel"][atype]
                ))

            #
            # The internal signature and arguments are just a list of
            # extern.anames joined together.

            func_text = {
                "rtype":   TYPE2SOURCE["chapel"][extern.rtype],
                "pars":    ", ".join(pars),
                "conversion": conversion,
                "pars_internal": ", ".join(extern.anames),
                "args_internal": ", ".join(extern.anames),
                "ename":   extern.ename,
                "fbody":   extern.doc
            }

            source += tmpl_internal % func_text
            source += tmpl % func_text

        return source

