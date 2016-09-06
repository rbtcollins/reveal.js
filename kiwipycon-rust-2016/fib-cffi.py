#!/usr/bin/pypy

import os.path

from _fibcffi import ffi
ffi.dlopen(
    os.path.expanduser("~/.multirust/toolchains/nightly-x86_64-unknown-linux-gnu/lib/libstd-411f48d3.so"))
lib = ffi.dlopen("rust-demos/target/release/libdemos.so")
for _ in range(20000):
    x = lib.fib(60)
print(x)
