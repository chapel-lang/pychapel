
.. _sec-getting-started:

Getting Started
===============

This section covers installation of pyChapel and required software packages,
introduces the "pych" utility and provides a "hello world" example of using
pyChapel.

System Requirements
~~~~~~~~~~~~~~~~~~~

* Linux-64 host system (Ubuntu 16.04 is shown here). Mac OS-X is not yet supported.
* Python-2.7 (the later, the better), with pip. Python-3 is not yet supported.
* Support for Chapel "Quickstart" on the host. See `Prerequisites <https://chapel-lang.org/docs/latest/usingchapel/prereqs.html>`_

Installation
~~~~~~~~~~~~

The steps for installing pyChapel and the software packages it depends upon are
fairly straightforward. The following provides a setup guide on a Ubuntu-16.04
host system.

The pyChapel Python module itself is available from PyPi.
Make sure you are using the Python2 version of Pip and any other Python utilities.
We recommend using Pip's "user install" option as shown here, but those familiar
with other Python2 virtual environments may adapt these instructions accordingly.
A Pip "user install" will install pyChapel under ``$HOME/.local``, so make sure that
``$HOME/.local/bin`` is near the front of your PATH.

Install pyChapel and dependencies from PyPi::

  $ pip install --user "numpy>=1.14" "future>=0.15.2" pyChapel

Run the pyChapel self-check. Note the "Missing Chapel lib" dir location::

  $ pych -k     # if "command not found", make sure $HOME/.local/bin is in PATH
    Checking installation...
    * Templates
    * Object Storage
    * Libraries
    ERR: Missing Chapel lib file(libchpl.a) in dir(/home/chapeluser/.local/share/pych/lib)
    ERR: Missing Chapel lib file(main.o) in dir(/home/chapeluser/.local/share/pych/lib)
    * Commands

PyChapel requires the Chapel compiler and runtime, which must be built from source
to work with pyChapel. 

Get the Chapel source from Github::

  $ cd $HOME    # For example- any location that will not get accidentally deleted
  $ git clone git@github.com:chapel-lang/chapel.git

Note the location::

    $HOME/chapel  (in this example)

Add the following to your shell environment::

    (.bashrc, for example)

    #
    # Setup Chapel environment
    #
    # CHPL_HOME=Chapel source location
    #
    export CHPL_HOME=$HOME/chapel   # in this example
    export CHPL_LIBMODE=shared
    source $CHPL_HOME/util/quickstart/setchplenv.bash
    #
    # Add Pip/Python "user install" bin to PATH, if needed
    #
    export PATH=$HOME/.local/bin:$PATH

Build the Chapel compiler and run-time system::

    (Make sure the above shell environment has been set up first.)

  $ cd $CHPL_HOME
  $ make

See `Quickstart <https://chapel-lang.org/docs/latest/usingchapel/QUICKSTART.html>`_ for more
information about building Chapel.


Chapel run-time libraries
-------------------------

The Chapel build leaves the run-time libraries in a platform-dependent internal subdirectory.
Fortunately, a utility is provided that returns the location.
The library files must be copied into pyChapel's "Chapel lib" internal subdirectory: the
"Missing Chapel lib" dir location reported by ``pych -k``
(for example, ``$HOME/.local/share/pych/lib``).

Copy the run-time libraries from Chapel into pyChapel::

  $ libchpl=`$CHPL_HOME/util/config/compileline --main.o`
  $ libpych=$HOME/.local/share/pych/lib     # from "pych -k"
  $ cp `dirname $libchpl`/* $libpych

Re-run the pyChapel self-check::

  $ pych -k
    Checking installation...
    * Templates
    * Object Storage
    * Libraries
    * Commands

  # no "Missing Chapel lib files"


Hello World
~~~~~~~~~~~

You should now be ready to try it out, create a file named `hw.py` with the
following content:

.. literalinclude:: /examples/test_chapel_inline.py
   :language: python
   :lines: 1-11

Then try running it::

  $ python hw.py

This should then print out the classic::

  Hello, world

Continue to :ref:`sec-usage` for examples of something slightly more interesting
than `Hello, world`.
