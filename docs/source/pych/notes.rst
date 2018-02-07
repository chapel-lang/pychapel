Miscellanous Notes
==================

Developer Notes
~~~~~~~~~~~~~~~

A couple of extra packages comes in handy if you want to contribute to pyChapel.

  pip install Sphinx sphinx-rtd-theme

Compiling Chapel modules into libraries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Compiling Chapel code into shared libraries is a multistep process:

1. Modify your Chapel code, make it "exportable".
2. Compile your Chapel code into an archive.
3. Link the archive with `libchpl` and creature a loadable shared object.

Let us go through an example, describing a couple of caveats and what needs to
be modified. 

Step 1: Code Modification
-------------------------

Take the following module:

.. literalinclude:: /examples/sfiles/chapel/hellolib.chpl
   :language: chapel

In order to compile this into a library the following changes must be made:

1. Remove the `main` procedure.
2. Add `export` to the procedures you want to access.
3. If an exported procedure relies on type-inference (which cannot be resolved at compile-time), then do one of the following.

   3a. Change the procedure by adding a type-signature.

   3b. Export a typed wrapper-procedure instead of the actual procedure.

The resulting modification to the module could look like this:

.. literalinclude:: /examples/sfiles/chapel/hellolib.exported.chpl
   :language: chapel

.. note :: Adding the return-type is a caveat introduced by `pychapel` not by the Chapel compiler.  The `pych` command and `pyChapel` is currently not able to infer the return-type. You therefore need to add the return-type of procedures in your Chapel module if you want to use `pych` to compile your Chapel module into a Python module.

Step 2: Compilation
-------------------


Step 3: Linking
---------------


