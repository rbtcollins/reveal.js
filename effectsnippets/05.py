from __future__ import print_function

__metaclass__ = type

import os
import sys

from effect import (
    ComposedDispatcher,
    Effect,
    TypeDispatcher,
    base_dispatcher,
    sync_perform,
    sync_performer,
    )
import testtools



class Print:
    def __init__(self, line):
        self.line = line


@sync_performer
def real_print(dispatcher, print_):
    print(print_.line)
    sys.stdout.flush()


real_interpreter = ComposedDispatcher([
    TypeDispatcher({
        Print: real_print,
        }),
    base_dispatcher])


def program():
    return Effect(Print('What... is your quest?'))


if __name__ == '__main__':
    sync_perform(real_interpreter, program())


class Tests(testtools.TestCase):

    def test_print(self):
        outputs = []
        @sync_performer
        def test_print(dispatcher, print_):
            outputs.append(print_.line)

        test_interpreter = ComposedDispatcher([
            TypeDispatcher({
                Print: test_print,
                }),
            base_dispatcher])

        dispatcher = test_interpreter
        sync_perform(dispatcher, program())
        self.assertEqual(["What... is your quest?"], outputs)
