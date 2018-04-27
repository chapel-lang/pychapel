// Wrapper around the pych_array c-struct
// to access NumPy arrays provided by the PyChapel
// Python module
use Random;

param PYCH_MAXDIM: int(32)= 16;

extern record pych_array {
    var two:int(32);
    var nd:int(32);
    var typekind:int(8);
    var itemsize:int(32);
    var flags:int(32);
    var shape:PYCH_MAXDIM*int(32);
    var strides:PYCH_MAXDIM*int(32);
    var ptr_d:_ddata(real);
}

proc pprint_pych_array(arr: pych_array) {
    writeln("[");
    writeln("  two=", arr.two, ",");
    writeln("  nd=", arr.nd, ",");
    writeln("  typekind=", arr.typekind, ",");
    writeln("  itemsize=", arr.itemsize, ",");

    write("  shape=");
    for idx in 1..PYCH_MAXDIM {
        write(arr.shape(idx));
        if (PYCH_MAXDIM != idx) {
            write(",");
        }
    }
    writeln("");
    write("  stride=");
    for idx in 1..PYCH_MAXDIM {
        write(arr.strides(idx));
        if (PYCH_MAXDIM != idx) {
            write(",");
        }
    }
    writeln("");
    writeln("  ptr_d=", arr.ptr_d);
    writeln("]");
}

proc rangify(shape) where isTuple(shape) {
    proc tail(first, remainder...) {
        return remainder;
    }
    if (shape.size == 1) {
        return (0..shape(1):int(64),);
    } else {
        return ((0..shape(1):int(64)), (...rangify(tail((...shape)))));
    }
}

proc pych_to_chpl1D(arr: pych_array) {
    pragma "no auto destroy"
    var dom = {0..(arr.shape(1):int(64)-1)};

    var stride = (1,);
    var block = (1,);

    var ret = new unmanaged DefaultRectangularArr(
        eltType = real,                 // Element type
        rank = dom.rank,                // Rank
        idxType = dom.idxType,          // Index type of domain
        stridable = dom.stridable,      // Boolean, can we stride?
        dom = dom._value,               // The underlying class implementation
        noinit_data = true              // Prevent overwriting your data
    );     
   
    dom._value.add_arr(ret);

    for i in 1..arr.nd {
        // TODO: Is this conversion from bytes to elements correct?
        //ret.str(i) = (arr.strides(i):int(64) / (arr.itemsize));
        ret.str(i) = 1;
    }
    //writeln("Strides");
    //for str in ret.str {
    //    writeln(str);
    //}
    for i in 1..arr.nd {
        // TODO: Is this conversion from bytes to elements correct?
        // The block seems to be what NumPy call strides.
      if (arr.strides(i):int(64) != arr.itemsize) {
        writeln("warning: pyChapel may not support unusually strided ndarrays");
      }
      ret.blk(i) = (arr.strides(i):int(64) / arr.itemsize);
    }
    //ret.blk = block;

    // get offsets from domain
    for param i in 1..dom.rank {
        ret.off(i) = dom._value.dsiDim(i).low;
    }

    ret.data = arr.ptr_d;
    ret.origin = 0; // I believe 'origin' is the c ptr offset
    ret.computeFactoredOffs();
    ret.initShiftedData();

    return ret;
}

proc pych_to_chpl2D(arr: pych_array) {
    pragma "no auto destroy"
    var dom = {(...rangify(arr.shape))};

    //writeln(pych_to_chplT(arr));
    var stride = (1, 1);
    var block = (3, 1);

    var ret = new unmanaged DefaultRectangularArr(
        eltType = real,                 // Element type
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
    //ret.str = stride;
    
    for i in 1..arr.nd {
        ret.str(i) = arr.strides(i):int(64);
    }

    // I'm not totally sure what this one is. I think it's the size of a row of data.
    // You can test this by writing code like:
    //var x = [1..10, 10..20]: int;
    //writeln("What is this?");

    ret.blk = block;

    // get offsets from domain
    for param i in 1..dom.rank {
        ret.off(i) = dom._value.dsiDim(i).low;
    }

    ret.data = arr.ptr_d;
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

