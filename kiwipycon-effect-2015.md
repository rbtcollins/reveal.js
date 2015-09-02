## Functionalish programming
## with Effect

Slides at https://github.com/rbtcollins/reveal.js

<small>Robert Collins  
rbtcollins@hp.com  
@rbtcollins (Twitter)</small>



## Chris Armstrong

@radix


## Effect

https://pypi.python.org/pypi/effect

https://github.com/python-effect/effect


## Motivation 1

note:
code with predictable behaviours
Fast/Easy testing of same code
Reliable testing of same code (purity)


Whats wrong with this code?

```
print("What... is your quest?")
```


```
$ python ./01.py  > /dev/full
Exception ignored in: <_io.TextIOWrapper name='<stdout>' mode='w' encoding='UTF-8'>
OSError: [Errno 28] No space left on device
```


```
$ echo $?
0
```

http://bugs.python.org/issue5319


## Undefined behaviour

global state <!-- .element: class="fragment" -->


## Innards

1. name lookup: print <!-- .element: class="fragment" -->
2. marshall args <!-- .element: class="fragment" -->
3. call it <!-- .element: class="fragment" -->
4. name lookup: sys.stdout <!-- .element: class="fragment" -->
5. .write <!-- .element: class="fragment" -->
6. output buffered <!-- .element: class="fragment" -->

note:
1. **global**
2. **local** 
3. **local**
4. **global**
5. **local**
6. **global**


## Testing this code?

1. Monkeypatching <!-- .element: class="fragment" -->
2. Subprocesses <!-- .element: class="fragment" -->
3. IO Redirection <!-- .element: class="fragment" -->


How might we fix this?


```
import sys
print("What... is your quest?", file=sys.stdout)
sys.stdout.flush()
```


```
Traceback (most recent call last):
  File "./02.py", line 3, in <module>
    sys.stdout.flush()
OSError: [Errno 28] No space left on device
Exception ignored in: <_io.TextIOWrapper name='<stdout>' mode='w' encoding='UTF-8'>
OSError: [Errno 28] No space left on device
```


```
echo $?
1
```


Testing is still undesirable


## Haskell

note:
Terms to solve problems we do not have.


## Monads

note:
such as..


```
import sys
fred = 1
sys.modules['__main__'].fred = 2
print("%s" % fred)
```

Note:
We know in Python, but Haskell is pure math: similar code in haskell is not an
instruction to do something, its a statement about how to derive a value if the
value is needed.


```
do x1 <- action1
   x2 <- action2
   action3 x1 x2
```


```
action1 >>=
  \ x1 -> action2 >>=
    \ x2 -> action3 x1 x2
```

\>\>= is an infix function called bind.


## Python transliteration

```
def _1(x1):
    def _2(x2):
        return action3(x1, x2)
    return _2(action2())
result = _1(action1())
```


Beep, wrong


## Type inference

\>\>= is polymorphic on its left hand argument. We are missing the monad.


```
class Monad:
    def __init__(self, v):
        self.v = v
    def bind(self, f):
        return f(self, self.v)
    def unit(self, v):
        return self.__class__(v)
```


```
def action1(m): return m.unit(1)
def action2(m): return m.unit(2)
def action3(m, x, y): return m.unit(x+y)
```


```
def _1(m1, x1):
    def _2(m2, x2):
        return action3(m2, x1, x2)
    return action2(m1).bind(_2)
m = Monad(None)
lastline = action1(m).bind(_1)
print(lastline.v)
```



## So that style is testable right?


## Not really

1. actions can do anything <!-- .element: class="fragment" -->
2. stacks of lambdas are hard to reason about <!-- .element: class="fragment" -->



## Better title

http://www.haskellforall.com/2012/07/purify-code-using-free-monads.html

approximated in Python by @radix

note:
Chris had read that and it may or may not be part of the inspiration for Effect.



## Free Monad

note:
The name makes sense but the explanation is longer than this talk.


## Make a language to express actions

```
class Print:
    def __init__(self, line):
        self.line = line
```


## Write pure code

```
def program():
    return Effect(Print('What... is your quest?'))
```

1. Return generators or Effects
2. Functions accept a single parameter


## Write an interpreter

```
@sync_performer
def real_print(dispatcher, print_):
    print(print_.line)
    sys.stdout.flush()

real_interpreter = ComposedDispatcher([
    TypeDispatcher({
        Print: real_print,
        }),
    base_dispatcher])
```

note:
We have split out business logic and things that must be impure



## So what about testing?


## Write an interpreter

```
def test_print(self):
    outputs = []
    @sync_performer
    def perform_test(dispatcher, print_):
        outputs.append(print_.line)
```

Cannot assert here in the general case.


```
    test_interpreter = ComposedDispatcher([
        TypeDispatcher({
            Print: perform_print,
            }),
        base_dispatcher])

    dispatcher = test_interpreter
    sync_perform(dispatcher, program())
    self.assertEqual(["What... is your quest?"], outputs)
```


1. ~~Monkeypatching~~ <!-- .element: class="fragment" -->
2. ~~Subprocessess~~ <!-- .element: class="fragment" -->
3. ~~IO Redirection~~ <!-- .element: class="fragment" -->



## We used the production API 

Little awkward with closures etc.

note:
Arguably a design defect (see the free monad blog post in haskell) - being able
to pass a RealWorld equivalent in would allow each test interpeter to be
independent without closures.


## Dedicated testing API


```
effect.testing.SequenceDispatcher
```


```
def test_print(self):
    sequence = SequenceDispatcher([
        (Print('What... is your quest?'), lambda _:None),
        ])

    with sequence.consume():
        sync_perform(sequence, program())
```


```
Print = namedtuple("Print", "line")
```

note:
Named tuples because SequenceDispatcher uses equality.


```
Readline = namedtuple("Readline", "")

@sync_performer
def real_readline(dispatcher, readline):
    return sys.stdin.readline()

real_interpreter = ComposedDispatcher([
    TypeDispatcher({
        Print: real_print,
        Readline: real_readline,
        }),
    base_dispatcher])
```


```
def echo():
    result = Effect(Print('What... is your quest?')).on(
        success=lambda _: Effect(Readline())).on(
        success=lambda r: Effect(Print(r)))
    return result
```


```
@given(st.text())
def test_echo(self, line):
    sequence = SequenceDispatcher([
        (Print('What... is your quest?'), lambda _:None),
        (Readline(), lambda _:line),
        (Print(line), lambda _:None),
        ])

    with sequence.consume():
        sync_perform(sequence, echo())
```



## What about loops etc?


## And Now for Something Completely Different


```
from effect.do import do
...
@do
def echo():
  yield Effect(Print('What... is your quest?'))
  line = yield Effect(Readline())
  yield Effect(Print(line))
```


```
with sequence.consume():
  dispatcher = ComposedDispatcher([
  sequence,
  base_dispatcher,
  ])
  sync_perform(dispatcher, echo())
```



## Loops

```
@do
def challenge():
    line = None
    while line != 'To seek the Holy Grail.\n':
        yield Effect(Print('What... is your quest?'))
        line = yield Effect(Readline())
    yield Effect(Print('What... is your favourite colour?'))
```


```
@given(st.text())
def test_challenge(self):
    sequence = SequenceDispatcher([
        (Print('What... is your quest?'), lambda _:None),
        (Readline(), lambda _: line),
        (Print('What... is your quest?'), lambda _:None),
        (Readline(), lambda _:'To seek the Holy Grail.\n'),
        (Print('What... is your favourite colour?'), lambda _:None),
        ])
```



## Returning from generators

```
from effect.do import do_return

@do
def challenge():
    line = None
    while line != 'To seek the Holy Grail.\n':
        yield Effect(Print('What... is your quest?'))
        line = yield Effect(Readline())
    yield do_return(line)
```


```
@given(st.text())
def test_challenge(self):
      sequence = [
	  (Print('What... is your quest?'), lambda _:None),
	  (Readline(), lambda _: line),
	  (Print('What... is your quest?'), lambda _:None),
	  (Readline(), lambda _:'To seek the Holy Grail.\n'),
	  ]

      result = perform_sequence(sequence, challenge())
      self.assertEqual(result, 'To seek the Holy Grail.\n')
```



## Questions?

Example code: 
https://github.com/rbtcollins/reveal.js/tree/master/effectsnippets

* Robert Collins
* @rbtcollins
* lifeless on freenode
* rbtcollins@hp.com
