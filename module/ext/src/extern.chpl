module Pythonic {

    // Wrapper around the pych_array c-struct
    // to access NumPy arrays provided by the PyChapel
    // Python module
    extern record pych_array {
        var two:int(32);
        var nd:int(32);
        // typekind
        var itemsize:int(32);
        var flags:int(32);

        //  shape
        // strides
        var data:_ddata(real);
    }

    proc pych_to_chpl(arr: pych_array) {
        pragma "no auto destroy"
        var dom = {0..1, 0..4};
        var stride = (1, 1);
        var block = (5, 1);

        var ret = new DefaultRectangularArr(
            eltType = real,   // Element type
            rank = dom.rank,                // Rank
            idxType = dom.idxType,          // Index type of domain
            stridable = dom.stridable,      // Boolean, can we stride?
            dom = dom._value,               // The underlying class implementation
            noinit_data = true              // Prevent overwriting your data
        );     
        dom._value.add_arr(ret);

        // rank*int tuples

        // stride for each dimension
        // you might be able to get this out of the domain instead.
        ret.str = stride;

        // I'm not totally sure what this one is. I think it's the size of a row of data.
        // You can test this by writing code like:
        /*
         var x = [1..10, 10..20] int;
         writeln(x._value.blk);
        */
        ret.blk = block;

        // get offsets from domain
        for param i in 1..dom.rank {
            ret.off(i) = dom._value.dsiDim(i).low;
        }

        ret.data = arr.data;
        ret.origin = 0; // I believe 'origin' is the c ptr offset
        ret.computeFactoredOffs();

        // if you're having segfaults, look into this method. You can also try
        // compiling with '-searlyShiftData=false' to disable this method.
        ret.initShiftedData();

        // only returns the underlying class, still need to turn it into a 
        // first-class chapel array. I'm not sure why exactly, but something
        // about the way we return arrays here performs a copy and changes
        // made to the array aren't reflected in the c pointer.
        return ret;
    }

    proc main() {
        var foo: pych_array;
        foo.two = 2;
        foo.nd = 2;
        foo.data = _ddata_allocate(real, 10);
        
        var ret = pych_to_chpl(foo);
        var arr = _getArray(ret);
        arr = 4.0;
        arr += 1.0;
        writeln(arr);
    }

}
