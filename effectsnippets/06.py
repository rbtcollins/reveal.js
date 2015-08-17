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


def program():
    return Effect(Print('What... is your quest?'))


def echo():
    result = Effect(Print('What... is your quest?')).on(
        success=lambda _: Effect(Readline())).on(
        success=lambda r: Effect(Print(r)))
    return result


if __name__ == '__main__':
    sync_perform(real_interpreter, echo())


class Tests(testtools.TestCase):

    def test_print(self):
        sequence = SequenceDispatcher([
            (Print('What... is your quest?'), lambda _:None),
            ])

        with sequence.consume():
            sync_perform(sequence, program())

    @given(st.text())
    def test_echo(self, line):
        sequence = SequenceDispatcher([
            (Print('What... is your quest?'), lambda _:None),
            (Readline(), lambda _:line),
            (Print(line), lambda _:None),
            ])

        with sequence.consume():
            sync_perform(sequence, echo())
