from __future__ import print_function
import numpy as np
from pych.extern import FromC

@FromC()
def pass_it(x=np.ndarray, y=np.ndarray):
    r"""
    printf("Printing stuff...\n");
    pych_pprint_array(x);
    pych_pprint_array(y);
    printf("Create pointers...\n");
    double* x_cast = x->ptr_d;
    double* y_cast = y->ptr_d;
    printf("Loop through...\n");
    printf("Where is void: x=%p, y=%p\n", x->ptr_d, y->ptr_d);
    for(int i=0; i<x->shape[0]; i++) {
        printf("i=%d, ", i);
        printf("x=%f, y=%f", *x_cast, *y_cast);
        printf("\n");
        *x_cast = *x_cast + *y_cast;
        y_cast++;
        x_cast++;
    }
    printf("Done.\n");
    """
    return None

if __name__ == "__main__":
    r = np.ones(10)
    print(pass_it(r, np.arange(0,10, dtype=np.float64)))
    print(r)
