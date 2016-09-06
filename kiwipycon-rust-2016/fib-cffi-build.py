#!/usr/bin/pypy
from cffi import FFI
ffi = FFI()
ffi.set_source("_fibcffi", None)
ffi.cdef("""
    long fib(long n);
""")
ffi.compile(verbose=True)
