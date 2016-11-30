.. _sec-getting-started:

Getting Started
===============

This section covers installation of pyChapel and required software packages,
introduces the "pych" utility and provides a "hello world" example of using
pyChapel.

Installation
~~~~~~~~~~~~

The steps for installing pyChapel and the software packages it depends upon is
fairly straightforward. The following provides a setup guide on a Ubuntu-linux system.

Depending on your system the commands might be slightly different but the 
should provide the gist of what is required.

pyChapel depends on the pyChapel Python module itself which is available via
PyPi. Additionally the Chapel compiler and a library compiled with the compiler
is required.

Installing pyChapel::

  pip install numpy argparse pyChapel

Build and install Chapel from source::

  cd ~
  git clone git@github.com:chapel-lang/chapel.git

Add this or equivalent to your environment::

  #
  # Setup Chapel
  #
  CWD=`pwd`
  export CHPL_REGEXP=none
  export CHPL_MEM=cstdlib
  export CHPL_GMP=none
  export CHPL_TASKS=fifo
  export CHPL_LIBMODE=shared
  cd ~/chapel/ && source ~/chapel/util/setchplenv.bash
  cd $CWD

Reload your environment, then build the compiler::

  cd ~/chapel
  make

After building the two files: "libchpl.a" and "main.o" library should be available here::

  ~/chapel/lib/linux64/gnu/arch-native/loc-flat/comm-none/tasks-fifo/tmr-generic/mem-cstdlib/atomics-intrinsics/gmp-none/hwloc-none/re-none/wide-struct/fs-none/

Copy these to the "lib" library of pyChapel. Using a default install this can be
done with the command::

  find ~/chapel/lib/ -depth -type f -exec bash -c 'cp $0 /usr/local/share/pych/lib/' {} \;

After going through these steps the installation can be verified by running the
"pych" command::

  pych --check

Hello World
~~~~~~~~~~~

You should now be ready to try it out, create a file named `hw.py` with the
following content:

.. literalinclude:: /examples/test_chapel_inline.py
   :language: python
   :lines: 1-12

Then try running it::

  python hw.py

This should then print out the classic::

  Hello, world

Continue to :ref:`sec-usage` for examples of something slightly more interesting
than `Hello, world`.
