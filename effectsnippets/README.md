# Index

Examples from my talk about Effect. Use with Python3.somethingrecent. Python 2.7 has even more bugs :)

## 00.py

Minimal valid python file. Run with python 00.py > /dev/full

Expected exit code of 0.

## 01.py

Minimal valid python file performing output IO. Run with 01.py > dev/full

Does not work due to http://bugs.python.org/issue5319

Expected exit code of non-zero.
Actual exit code of zero.

## 02.py

01.py bugfixed to show errors properly. Run as before.

Expected exit code of non-zero.
Actual exit code of non-zero.

## 03.py

Ordering as a thing.


## 04.py

Simple monad in Python - terrible but educational.

## 05.py

Simple effect based echo with pure interpreter based tests.

Run tests via python -m testtool.run 05.py

## 06.py

Simple effect based echo with effect.testing tests.

Run tests via python -m testtool.run 06.py
