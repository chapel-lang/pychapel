config const n = 10;
const drange = 0..n-1;

var ptr : _ddata(int) = _ddata_allocate(int, n);

proc printDData() {
  write("cptr = [ ");
  for i in 0..n-2 do write(ptr[i], ", ");
  writeln(ptr[n-1], " ]");
}

export yoyo
proc yoyo(spin: _ddata(real(64))) {
    return spin;
}

/*
export yolo
proc yolo(spin: _ddata(void)) {
    var zoom: _cast(_ddata(real(64)), spin);
    return spin;
}*/

export lolo
proc lolo(spin: _ddata(int(64))) {
    var zoom: _cast(_ddata(real(64)), spin);
    //var zoom: __primitive("cast", _ddata(real(64)), spin);
    return spin;
}

proc convert(ref foo : _ddata(int), d, stride: d.rank*int, block: d.rank*int) {
  var ret = new DefaultRectangularArr(eltType=foo.eltType, rank=d.rank,
      idxType=d.idxType,     // index type of domain
      stridable=d.stridable, // boolean, can we stride?
      dom=d._value,          // d._value is the underlying class implementation
      noinit_data=true);     // prevent overwriting your data

  d._value.add_arr(ret);
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
  for param i in 1..d.rank {
    ret.off(i) = d._value.dsiDim(i).low;
  }
  
  ret.data = foo;
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

printDData();
for i in drange do ptr[i] = i;
printDData();

var ret = convert(ptr, {1..2, 1..5}, (1,1), (5,1));

// the actual chapel array.
var arr = _getArray(ret);
writeln(arr);

arr[1,1] = 11;
ptr[n-1] = -5;
forall a in arr do a = a*a;
writeln(arr);
printDData();
