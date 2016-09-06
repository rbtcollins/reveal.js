#!/usr/bin/python3.5
def fib(n: int):
    fibs = [1, 1]
    for _ in range(max(n-2, 0)):
        fibs.append(fibs[-1] + fibs[-2])
    return fibs[n-1]
print("%s" % fib(38))
