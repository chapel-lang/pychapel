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
Encapsulation for invoking system compiler.
"""
from builtins import object
# pylint: disable=too-few-public-methods
# The Compiler object encapsulates compiler setup and it is only supposed
# to take care of one well-define action: calling the compiler, it is
# therefore perfectly fine that it only has a single method.

from subprocess import Popen, PIPE
import tempfile
import hashlib
import pprint
import time
import os
import re

from pych.exceptions import CompilationError
from pych.utils import prepend_path
import pych.specializer
from pych.types import CHPL2PY

LANG2EXT = {
    "c":        ".c",
    "chapel":   ".chpl"
}

class Compiler(object):
    """
    Use this class to compile source-code to shared libraries,
    loadable by the ObjectStore.
    """

    def __init__(self, options):
        self._options = {}

        # Set "root_path" use "root_path": "" in JSON to use CWD.
        self._options["root_path"] = os.path.abspath(options["root_path"])

        # Paths
        for path in ["output_path", "lib_path", "inc_path"]:
            self._options[path] = prepend_path(
                self._options["root_path"],
                options[path]
            )

        # Includes
        self._options["includes"] = ""
        for include_path in options["includes"]:
            self._options["includes"] += '-I %s%s' % (
                prepend_path(self._options["root_path"], include_path),
                os.sep
            )

        # Compiler and linker flags
        self._options["cflags"] = " ".join(options["cflags"])
        self._options["lflags"] = " ".join(options["lflags"])

        # Use replements on these
        self._options["ctargets"] = " ".join(options["ctargets"]) % (
            self._options
        )

        self._options["ltargets"] = " ".join(options["ltargets"]) % (
            self._options
        )

        self._options["commands"] = [
            cmd % self._options for cmd in options["commands"]
        ]
        self._options["save_autogen"] = bool(options["save_autogen"])

    def __repr__(self):
        return pprint.pformat(vars(self))

    def compile(self, source, language, object_abspath, chplflags):
        """
        Compiles the given 'source' into a shared library.
        The result will be stored in object_abspath.

        :param str source: Sourcecode to compile.
        :param str language: Language of the sourcecode e.g. "c" or "chapel".
        :param str chplflags: string containing a concatentation of all flags
         passed along for chapel code to work
        :returns: Accumulation of all output and errors from compiler/linker
         commands as tuple(out, err).
        :rtype: tuple
        """

        all_out = ""
        all_err = ""

        with tempfile.NamedTemporaryFile(
            suffix=LANG2EXT[language],
            prefix="temp-",
            delete=self._options["save_autogen"]) as sfile_h:

            sfile_h.write(source)               # Dump the source out
            sfile_h.flush()

            archive_tmp_name = "asdf"
            with tempfile.NamedTemporaryFile() as tmp_fd:
                archive_tmp_name = tmp_fd.name

            for cmd in self._options["commands"]: # Execute commands
                cmd = cmd.replace("__CHPL_FLAGS__", chplflags)
                cmd = cmd.replace("__SFILE__", sfile_h.name)
                cmd = cmd.replace("__TMP_PATH__", archive_tmp_name)
                cmd = cmd.replace("__OBJECT_ABSPATH__", object_abspath)

                try:
                    process = Popen(cmd.split(), stdout=PIPE, stdin=PIPE)
                    out, err = process.communicate(source)
                except OSError as exc:
                    raise CompilationError(
                        cmd,
                        None,
                        exc
                    )

                all_out += out if out else ""
                all_err += err if err else ""

        return all_out, all_err

def parse_export_declarations(source):
    """Parse export declarations of Chapel code.

    :param source str: Source code to parse

    :rtype: tuple
    :returns: Tuple of lists (args, anames, atypes), `anames` is an ordered list
        of argument names, `atypes` and ordered list of argument types and `args`
        is equivalent to the zip(`anames`, `atypes`).
    """

    declarations = []

    for match in re.finditer("export.*?{", source, re.DOTALL):
        decl = ("".join(match.group(0)[6:].splitlines())).replace(" ", "")

        ename, decl = decl.split("proc", 1) # Get ename and strip from decl
        ename = ename.strip()               # Remove whitespace

        pname, decl = decl.split("(", 1)    # Get pname and strip from decl
        pname = pname.strip()               # Remove whitespace

        ename = ename if ename else pname   # Default ename to pname

        type_split = decl.split(":")        # Return type
        rtype = type_split[-1][:-1]
        has_rtype = rtype != ")"
        decl = decl[:-(len(rtype)+3)]       # Strip return type from decl
        if not has_rtype:
            rtype = None

        args = []
        anames = []
        atypes = []

        split_args = (arg.split(":", 1) for arg in decl.split(",") if arg)
        for aname, atype in split_args:
            anames.append(aname)
            atypes.append(atype)
            args.append((aname, atype))

        declarations.append({
            "ename": ename,
            "pname": pname,
            "rtype": rtype,
            "args": args,
            "atypes": atypes,
            "anames": anames
        })

    return declarations

def moduralize(source_file, output_file=None):
    """
    Compile the Chapel source file / module  into a Python module.
    This currently means create a Python module with all
    exported Chapel functions available in the Python module.

    :param chapel_sf str: Chapel source file.
    """

    py_spizer = pych.RT.specializers["python"]   # Grab specializers
    chpl_spizer = pych.RT.specializers["chapel"]

    module_tmpl = py_spizer.load("module.py")   # Grab templates
    func_tmpl = py_spizer.load("function.py")

    source = chpl_spizer.load(source_file)      # Load source-file source

    declarations = parse_export_declarations(   # Grab exported procedures
        source
    )

    # Create a source-file that will be added to "sfiles"
    src_hash = hashlib.md5()
    src_hash.update(source)

    wrap_sf = "%s.chpl" % src_hash.hexdigest()
    wrap_fp = os.sep.join([chpl_spizer.sfiles[0], wrap_sf])

    # TODO: Generate wrapper code for argument conversion
    #       For now we just write the "regular" code down.
    with open(wrap_fp, 'w') as wrap_fd:
        wrap_fd.write(source)

    # Generate Python code for the wrapped functions
    functions = []
    for decl in declarations:
        sfile = wrap_sf
        ename = decl["ename"]
        pname = decl["pname"]
        args = ", ".join([
            "%s=%s" % (aname, CHPL2PY[atype]) for aname, atype in decl["args"]
        ])
        rtype = CHPL2PY[decl["rtype"]]

        func = {
            "sfile": sfile,
            "ename": ename,
            "pname": pname,
            "args": args,
            "rtype": rtype,
            "extras": ""
        }
        functions.append(func_tmpl % func)

    module_src = module_tmpl % {
        "functions": "\n".join(functions),
        "module_name": "noname",
        "sfile": source_file,
        "gen_tstamp": int(time.time())
    }

    if not output_file:
        output_file = "a_out.py"

    with open(output_file, 'w') as output_fd:
        output_fd.write(module_src)

    # Try up the generated module, this will trigger hints to runtime
    # pylint: disable=unused-variable
    # this is fine, we just want the side-effects of importing
    # the module to trigger, we dont want to actually use it
    mod = __import__(output_file.replace(".py", ""), fromlist=[''])

    # Then materialize all hinted libraries
    for lib in pych.RT.hints:
        pych.RT.materialize(pych.RT.hints[lib][0])

    return (source_file, output_file, wrap_fp)
