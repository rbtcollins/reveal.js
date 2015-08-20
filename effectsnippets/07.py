from __future__ import print_function

__metaclass__ = type

from collections import namedtuple
import os
import sys

from effect import (
    ComposedDispatcher,
    Effect,
    Func,
    TypeDispatcher,
    base_dispatcher,
    sync_perform,
    sync_performer,
    )
from effect.do import do
from effect.testing import SequenceDispatcher
from hypothesis import given
import hypothesis.strategies as st
import testtools


Print = namedtuple("Print", "line")


Readline = namedtuple("Readline", "")


@sync_performer
def real_print(dispatcher, print_):
    print(print_.line)
    sys.stdout.flush()


@sync_performer
def real_readline(dispatcher, readline):
    return sys.stdin.readline()


real_interpreter = ComposedDispatcher([
    TypeDispatcher({
        Print: real_print,
        Readline: real_readline,
        }),
    base_dispatcher])


@do
def echo():
    yield Effect(Print('What... is your quest?'))
    line = yield Effect(Readline())
    yield Effect(Print(line))


if __name__ == '__main__':
    sync_perform(real_interpreter, echo())


class Tests(testtools.TestCase):

    @given(st.text())
    def test_echo(self, line):
        sequence = SequenceDispatcher([
            (Print('What... is your quest?'), lambda _:None),
            (Readline(), lambda _:line),
            (Print(line), lambda _:None),
            ])

        with sequence.consume():
            dispatcher = ComposedDispatcher([
                sequence,
                base_dispatcher,
                ])
            sync_perform(dispatcher, echo())
