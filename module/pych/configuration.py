"""
Loads and stores pyChapel configuration.
"""
# pylint: disable=maybe-no-member
# The configuration object does have the "__file__" member via the module.
# pylint: disable=too-few-public-methods
# The configuration wraps around the configuration state, access is provided
# through __getitem__ it is perfectly valid that it has few public methods.

import inspect
import glob
import json
import os

from pych.utils import info, warn, error, prepend_path

class Configuration(object):
    """
    Load pyChapel configuration from file and internalize configuration state.
    """

    PPRINT_IGNORE = ['empty', 'write_test']

    def __init__(self, config_fn=None):
        """

        :config_fn str: Path to configuration file.
        """

        if not config_fn:               # Load configuration
            config_path = []
            path = inspect.getmodule(self).__file__.split(os.sep)
            for directory in path:
                if directory == "lib" or directory == "local":
                    break
                config_path.append(directory)
            config_path += [
                "share",
                "pych",
                "config",
                "pych.json"
            ]
            config_fn = os.sep.join(config_path)

        config_raw = json.load(open(config_fn))
        config = config_raw

        # TODO: Configuration here should do whatever path-magic is needed...

        #
        # The paths in configuration file should just be made absolute... this
        # is too much complexity for simple thing.
        #

        #
        # Object store paths
        #
        root_path = config_raw["object_store"]["root_path"]
        if not root_path:             # Root-path defaults to cwd
            root_path = os.getcwd()
                                            # Search paths
        search_paths = dict((source, []) for source in config_raw["object_store"]["search_paths"])
        for source in config_raw["object_store"]["search_paths"]:
            for search_path in config_raw["object_store"]["search_paths"][source]:
                search_paths[source].append(prepend_path(
                    root_path, search_path
                ))
                                            # Output paths
        output_paths = dict((source, []) for source in config_raw["object_store"]["output_paths"])
        for source in config_raw["object_store"]["output_paths"]:
            output_path = config_raw["object_store"]["output_paths"][source]
            output_paths[source] = prepend_path(
                root_path,
                output_path
            )
        config["object_store"]["search_paths"] = search_paths
        config["object_store"]["output_paths"] = output_paths

        #
        # TODO: Specializer paths

        #
        # TODO: 
        self._config = config

    def __getitem__(self, index):
        return self._config[index]

    def pprint_specializers(self, stypes=['bfiles', 'sfiles', 'templates']):
        """Pretty-print specializer-configuration as described in pych.json."""
        
        for stype in stypes:    
            info("** Listing %s" % stype) 
            bdirs = self._config["specializers"][stype]
            for slang in bdirs:
                for bdir in bdirs[slang]:
                    info("* %s %s(s) in '%s':" % (slang.title(), stype, bdir))
                    for fname in glob.glob("%s%s*" % (bdir, os.sep)):
                        if os.path.basename(fname) in self.PPRINT_IGNORE:
                            continue
                        info(os.path.basename(fname))
            info("** End of %s listing." % stype) 

    def pprint_objects(self, slangs=['c', 'chapel', 'tp']):
        """Pretty-print objects storage."""

        for slang in slangs:
            paths = self._config["object_store"]["search_paths"][slang]
            for path in paths:
                info("* %s objects in '%s':" % (slang.title(), path))
                for object_path in glob.glob("%s%s*" % (path, os.sep)):
                    if os.path.basename(object_path) in self.PPRINT_IGNORE:
                        continue
                    info(os.path.basename(object_path))
