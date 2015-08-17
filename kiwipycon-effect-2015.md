## Functionalish programming
## with Effect

Slides at https://github.com/rbtcollins/reveal.js

<small>Robert Collins  
rbtcollins@hp.com  
@rbtcollins (Twitter)</small>



## PREVIEW EDITION



## Chris Armstrong

@radix


## Effect

https://pypi.python.org/pypi/effect

https://github.com/python-effect/effect


## Motivation

note:
Bug free code
Testing of same code


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


## Python

```
def _1(x1):
    def _2(x2):
        return action3(x1, x2)
    return _2(action2())
result = _1(action1())
```


Beep, wrong


## Type inference

\>\>= is polymorphic on its left hand argument


```
class Monad:
    def __init__(self, f_or_v):
        if isinstance(f_or_v, Monad):
            f_or_v = f_or_v.f_or_v
        self.f_or_v = f_or_v
    def bind(self, f):
        return self.unit(f(self, self.f_or_v))
    def unit(self, f_or_v):
        return self.__class__(f_or_v)
```


```
def action1(m) -> Monad: return m.unit(1)
def action2(m) -> Monad: return m.unit(2)
def action3(m, x,y) -> Monad: return m.unit(x+y)
```


```
def r(f): return f.__annotations__['return']

m = Monad(None)
def _1(m1, x1):
    def _2(m2, x2):
        return action3(m2, x1, x2)
    return action2(m1).bind(_2)
lastline = action1(m).bind(_1)
print(lastline.f_or_v)
```



## So that style is testable right?


## Not really

1. actions can do anything <!-- .element: class="fragment" -->
2. stacks of lambdas are hard to reason about <!-- .element: class="fragment" -->



## Better title

http://www.haskellforall.com/2012/07/purify-code-using-free-monads.html

approximated in Python by @radix

note:
I have no idea whether Chris had read that post or not



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


## Write an interpreter

```
@sync_performer
def real_print(dispatcher, print_):
    print(print_.line)
    sys.stdout.flush()
```


```
real_interpreter = ComposedDispatcher([
    TypeDispatcher({
        Print: real_print,
        }),
    base_dispatcher])
```



## So what about testing?


## Write an interpreter

```
def test_print(self):
    outputs = []
    @sync_performer
    def test_print(dispatcher, print_):
        outputs.append(print_.line)
```

Cannot assert here


```
    test_interpreter = ComposedDispatcher([
        TypeDispatcher({
            Print: test_print,
            }),
        base_dispatcher])
```


```
    dispatcher = test_interpreter
    sync_perform(dispatcher, program())
    self.assertEqual(["What... is your quest?"], outputs)

```


## Injecting values in is hard

No affordances to facilitate this so far

note:
Arguably a design defect (see the free monad blog post in haskell)



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



Remaining plans

1. bigger example, for loop and actual logic
1. perf tests?
1. time check


##
functors

map over a context
fmap :: (a -> b) -> f a -> f b


identity 


**The code finishes before the job is finished**



# Original abstract
'everyone' knows that separating out IO and other side effects makes code easier to unit test. What if there were a Python library that helps do that systematically which you could use to make all your things better? There is. Come and find out more.

Chris Armstrong's Effect library is the library in question. I found this while digging into all the varied implementations of monads for Python (a generic concept that encapsulates the principle of IO and side effects) - and I'd like to share its beauty with other folk. Effect (https://pypi.python.org/pypi/effect) allows consistent separation of side effect (e.g. IO or even just global state changes) from the code that depends on those effects. Testing and reasoning about code becomes easier. But it can often be hard to get into such a system. Allow me to take you on a tour through how to change regular code into super testable code using Effect.



## Questions?

* Robert Collins
* @rbtcollins
* lifeless on freenode
* rbtcollins@hp.com
