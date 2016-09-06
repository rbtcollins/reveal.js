#!/usr/bin/python3.5
def fib(n: int):
    if n <= 2:
        return 1
    return fib(n-1) + fib(n-2)
print("%s" % fib(38))
