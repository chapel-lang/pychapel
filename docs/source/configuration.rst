Configuration
~~~~~~~~~~~~~

pyChapel uses a configuration file to setup the underlying machinary. This file
is called `pych.json` and is installed with the rest of the pyChapel package.
Which means it should be available in a location such as::

  $HOME/.local/share/pych/config/pych.json
  /usr/local/share/pych/config/pych.json

Or in some other location if a Python virtualenv is used when installing
pyChapel.  The configuration-file defines locations of resources, behaviour of
pyChapel and where output-files such as `.so` objects are stored and loaded
from.

The options should be self-explanatory, of most common interest might be these::

  low_level - Can be one of: [ERROR, WARNING, INFO, DEBUG]
  open_ahead - Load libraries as early as possible.

You will most likely not need to change any other options but you can experiment
with the `cflags` options in the ``compiler`` section. You can add, remove,
tweak options as you see fit.
