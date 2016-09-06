## Rust for Pythonistas

Slides at https://github.com/rbtcollins/reveal.js

<small>Robert Collins  
robertc@vmware.com  
@rbtcollins (Twitter)</small>



## Takeaways

1. Rust is great <!-- .element: class="fragment" -->
1. You can call it from Python <!-- .element: class="fragment" -->
1. You can use it for Pytohn extension modules <!-- .element: class="fragment" -->
1. It is enjoyable and productive <!-- .element: class="fragment" -->



## Commmon things

1. Great communities
2. General purpose
3. Nothing you can't write in them



## Python

1. Dynamic <!-- .element: class="fragment" -->
2. Gradually Typed <!-- .element: class="fragment" -->
3. Pithy <!-- .element: class="fragment" -->
4. Slow <!-- .element: class="fragment" -->


```
#!/usr/bin/python3.5
def fib(n: int):
    if n <= 2:
        return 1
    return fib(n-1) + fib(n-2)

print("%s" % fib(38))
```


```
fn fib(n: u64) -> u64 {
    if n <= 2 {
        1
    } else {
        fib(n - 1) + fib(n - 2)
    }
}

fn main() {
    println!("{}", fib(38))
}
```


## fib(38)
```
$ trial.sh fib.py fib-rust/release/build/fib-38
+--------------------------------------------------+
|+                                                 |
|+                                                 |
|+                                                 |
|+                                                 |
|+                                                 |
|+                                                 |
|+                                                 |
|+                                              x  |
|+                                           xx x  |
|+                                           xxxxxx|
|                                            |_AM| |
|A                                                 |
+--------------------------------------------------+
N           Min           Max        Median           Avg        Stddev
x  10         12.09         13.49         12.82        12.731    0.48153574
+  10          0.12          0.12          0.12          0.12          -nan
Difference at 95.0% confidence
        -12.611 +/- 0.31993
        -99.0574% +/- 2.513%
        (Student's t, pooled s = 0.340497)
```


## (though pypy helps)
```
$ trial.sh fib.py fib.pypy
+--------------------------------------------------+
|+                                                 |
|+                                                 |
|+                                                 |
|+                                                 |
|+                                                 |
|+                                          x      |
|+                                          x      |
|+                                          x      |
|+                                          x x    |
|+                                          x x xxx|
|                                           |_A_|  |
|A                                                 |
+--------------------------------------------------+
    N           Min           Max        Median           Avg        Stddev
x  10         12.19         13.79         12.65        12.726    0.56899912
+  10          1.27           1.3          1.29         1.286   0.010749677
Difference at 95.0% confidence
        -11.44 +/- 0.378107
        -89.8947% +/- 2.97114%
        (Student's t, pooled s = 0.402415)
```


## (but not that much)
```
$ trial.sh fib.pypy fib-rust/release/build/fib-38
+--------------------------------------------------+
|+                                                 |
|+                                                 |
|+                                                 |
|+                                                 |
|+                                             x   |
|+                                             x   |
|+                                             x   |
|+                                             x x |
|++                                           xxxxx|
|                                              MA| |
|A|                                                |
+--------------------------------------------------+
    N           Min           Max        Median           Avg        Stddev
x  10          1.31          1.41          1.34         1.354   0.030623158
+  10          0.11          0.13          0.11         0.114   0.006992059
Difference at 95.0% confidence
        -1.24 +/- 0.0208695
        -91.5805% +/- 1.54132%
        (Student's t, pooled s = 0.0222111)
```


## All together
```
$ trial.sh rust c pypy py
+--------------------------------------------------+
|*   *                                % %          |
|*   *                                %%%  %%%%   %|
|A                                                 |
|A                                                 |
|    A                                             |
|                                     |___AM__|    |
+--------------------------------------------------+
    N           Min           Max        Median           Avg        Stddev
x  10          0.12          0.18          0.15          0.15   0.017638342
+  10          0.13          0.16          0.14         0.142  0.0078881064
No difference proven at 95.0% confidence
*  10          1.58          1.71          1.68         1.662    0.04184628
Difference at 95.0% confidence
        1.512 +/- 0.0301713
        1008% +/- 20.1142%
        (Student's t, pooled s = 0.0321109)
%  10         15.09         19.87         16.92         16.76     1.5557206
Difference at 95.0% confidence
        16.61 +/- 1.03368
        11073.3% +/- 689.119%
        (Student's t, pooled s = 1.10013)
```



## Rust
1. Static <!-- .element: class="fragment" -->
2. Duck typed <!-- .element: class="fragment" -->
3. Safe <!-- .element: class="fragment" -->
4. Fast <!-- .element: class="fragment" -->
5. Explicit compilation <!-- .element: class="fragment" -->
6. Structured returns  <!-- .element: class="fragment" -->
7. Still minimal <!-- .element: class="fragment" -->

note:
Every type is fully defined at link time; there's no such thing as assigning a
new method descriptor at runtime and using it. There is runtime dispatch -
'trait objects'. Data races exist in Python. Very fast - use the stack entirely
and the heap as needed. cargo build is <3. Growing features through a community
process.


## Basics
1. rustfmt <!-- .element: class="fragment" -->
2. Cargo <!-- .element: class="fragment" -->


## Some code

```
use std::iter;

struct Fib {
    one_back: u64,
    current: u64
}

impl Fib {
    fn new() -> Fib {
        Fib {one_back: 0, current: 1}
    }
}

impl iter::Iterator for Fib {
    type Item = u64;

    fn next(&mut self) -> Option<u64> {
        let result = self.one_back + self.current;
        self.one_back = self.current;
        self.current = result;
        Some(result)
    }
}

fn main() {
    println!("{:?}", Fib::new().take(5).collect::<Vec<_>>())
}
```

note:
We don't inherit from Iterator - we just implement it.
Type inference is used within functions but not across it.
No explit return needed - just the last evaluated expression.'


## Almost no inheritance
```
// From https://doc.rust-lang.org/book/traits.html
trait Foo {
        fn foo(&self) { println!("foo"); }
}

trait FooBar : Foo {
        fn foobar(&self);
}

struct Baz;

impl Foo for Baz {
}

impl FooBar for Baz {
        fn foobar(&self) { println!("foobar"); }
}

fn main() {
    let b = Baz {};
    b.foo();
    b.foobar();
}
```

note:
Two forms of inheritance shown here. Traits can depend on another trait -
'inherit' - but implementations are still separate. Trait methods can have
default bodies, but only take effect on impl.


## Safety
```
fn main() {
    let b = Baz {};
    let c = b;
    b.foo();
}

error[E0382]: use of moved value: `b`
  --> src/bin/badmv.rs:12:5
   |
11 |     let c = b;
   |         - value moved here
12 |     b.foo();
   |     ^ value used here after move
   |
```
note:
all the standard stuff - bounds checking, uninitialised variables etc.
The really interesting things are data race protection and mutability
protection. Here we've seen that by default rust moves structs on assignment :
very unlike the name binding that Python utilises.


```
fn main() {
    let mut b = Baz {};
    let c = &mut b;
    b.foo();
}

error[E0499]: cannot borrow `b` as mutable more than once at a time
  --> badborrow.rs:12:5
   |
11 |     let c = &mut b;
   |                  - first mutable borrow occurs here
12 |     b.foo();
   |     ^ second mutable borrow occurs here
13 | }
   | - first borrow ends here
```

note:
To have indirection like in Python use references - but here is one of the key
protections: there can only be one mut reference and no read references, or
read references and no mut reference.


## Lifetimes
```
#[derive(Debug)]
struct Bar<'a> {
    reference: &'a u64,
}

fn main() {
    let ok = &42;
    let mut b = Bar { reference: ok };
    {
        let bad = &666;
        b.reference = bad;
    }
    println!("{:?}", b);
}

error: borrowed value does not live long enough
  --> lifetime.rs:10:20
   |
10 |         let bad = &666;
   |                    ^^^
   |
note: reference must be valid for the block suffix following statement 1 at 8:38...
  --> lifetime.rs:8:39
   |
8  |     let mut b = Bar { reference: ok };
   |                                       ^
note: ...but borrowed value is only valid for the block suffix following statement 0 at 10:23
  --> lifetime.rs:10:24
   |
10 |         let bad = &666;
   |                        ^
```


## Exceptions / Structured Returns
Beautiful system for propogating errors.
See https://doc.rust-lang.org/book/error-handling.html

```
fn file_double<P: AsRef<Path>>(file_path: P) -> Result<i32, CliError> {
    let mut file = try!(File::open(file_path).map_err(CliError::Io));
    let mut contents = String::new();
    try!(file.read_to_string(&mut contents).map_err(CliError::Io));
    let n: i32 = try!(contents.trim().parse().map_err(CliError::Parse));
    Ok(2 * n)
}

fn caller() {
    match file_double("foobar") {
        Ok(n) => println!("{}", n),
        Err(err) => match err {
            CliError::Io => ...,
            CliError::Parse => ...,
            other => ...
    }
}
```

note:
try! will return early on Err types returned from the inner expression;
three key steps:
 - create an enum for your functions errors
 - impl Display and Error traits for the enum
   - delegate to wrapped types, handle local ones directly
 - impl From<wrapped> for wrapped types.


```
def file_double(file_path: PathLike):
    with open(file_path, 'rb') as f:
        contents - f.read()
    return int(contents) * n

def caller():
    try:
        print(file_double("foobar"))
    except IOError:
        ...
    except ParseError:
        ...
    except:
        ...
```


```
use std::error;
use std::fmt;
use std::io;

#[derive(Debug)]
pub enum BrokenRail {
    Netmap(netmap::NetmapError),
    IO(io::Error),
    BadPacket,
    NoIPV4Address,
}
```


```
impl fmt::Display for BrokenRail {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match *self {
            BrokenRail::Netmap(ref err) => err.fmt(f),
            BrokenRail::IO(ref err) => err.fmt(f),
            BrokenRail::BadPacket => write!(f, "Couldn't handle packet"),
            BrokenRail::NoIPV4Address => write!(f, "No IPV4 address on interface"),
        }
    }
}

impl error::Error for BrokenRail {
    fn description(&self) -> &str {
        match *self {
            BrokenRail::Netmap(ref err) => err.description(),
            BrokenRail::IO(ref err) => err.description(),
            BrokenRail::BadPacket => "Couldn't handle packet",
            BrokenRail::NoIPV4Address => "No IPV4 address on interface",
        }
    }

    fn cause(&self) -> Option<&error::Error> {
        match *self {
            BrokenRail::Netmap(ref err) => Some(err),
            BrokenRail::IO(ref err) => Some(err),
            BrokenRail::BadPacket => None,
            BrokenRail::NoIPV4Address => None,
        }
    }
}
```


```
impl From<netmap::NetmapError> for BrokenRail {
    fn from(err: netmap::NetmapError) -> BrokenRail {
        BrokenRail::Netmap(err)
    }
}

impl From<io::Error> for BrokenRail {
    fn from(err: io::Error) -> BrokenRail {
        BrokenRail::IO(err)
    }
}
```


## Planned features
1. Generators <!-- .element: class="fragment" -->
2. Co-routines, futures, await/async <!-- .element: class="fragment" -->
3. Incremental compilation <!-- .element: class="fragment" -->

note:
There are plenty of other things planned like MIR, a refactoring of the
internal compiler layers...


## Algorithms matter
```
# trial.sh fib.pypy fib-iterator.py fib-iterator.pypy rust-fib-iterator
+--------------------------------------------------+
|%+*                                               |
|%+*                                               |
|%+*                                               |
|%+*                                               |
|%+*                                               |
|%+*                                               |
|%+*                                   x           |
|%+*                                   xx          |
|%+*                                   xx          |
|%+*                                   xx    x   xx|
|                                    |__M_A___|    |
| A                                                |
|  A                                               |
|A                                                 |
+--------------------------------------------------+
    N           Min           Max        Median           Avg        Stddev
x  10          0.47          0.61          0.48         0.509   0.056065438
+  10          0.01          0.01          0.01          0.01 2.1951484e-10
Difference at 95.0% confidence
        -0.499 +/- 0.0372496
        -98.0354% +/- 7.31819%
        (Student's t, pooled s = 0.0396443)
*  10          0.02          0.02          0.02          0.02 4.3902967e-10
Difference at 95.0% confidence
        -0.489 +/- 0.0372496
        -96.0707% +/- 7.31819%
        (Student's t, pooled s = 0.0396443)
%  10             0             0             0             0             0
Difference at 95.0% confidence
        -0.509 +/- 0.0372496
        -100% +/- 7.31819%
        (Student's t, pooled s = 0.0396443)
```



## Installing Rust

https://github.com/rust-lang-nursery/rustup.rs



## Calling from Python

Lowest common denominator between Python and Rust is C.

Ownership gotchyas is the hardest thing.

http://mainisusuallyafunction.blogspot.co.nz/2014/08/calling-rust-library-from-c-or-anything.html (somewhat overly pessimistic...)
note:
I haven't got a canned detailed answer here but the core of it is to
write a small bit of unsafe code to pull structs being returned via the C API
out of Rust's ownership system, and to put them back in when they are being
freed.... and the next slide has a great example.


## Extension modules
See Tim McNamara's (@timClicks) poster on setuptools glue

The code in https://github.com/jbaiter/python-rust-fst is worth studying as an
example.



## RPC

Alternatively, use an RPC interface such as a JSON-HTTP server.

Higher overhead, particularly with slow to parse text protocols.



## FFI: Cargo.toml
```
[lib]
crate-type = ["cdylib"]
```


## FFI: Python
```
from cffi import FFI
ffi = FFI()
ffi.set_source("_fibcffi", None)
ffi.cdef("""
    long fib(long n);
""")
ffi.compile(verbose=True)
```

```
import os.path

from _fibcffi import ffi
ffi.dlopen(
    os.path.expanduser("~/.multirust/toolchains/nightly-x86_64-unknown-linux-gnu/lib/libstd-411f48d3.so"))
lib = ffi.dlopen("rust-demos/target/release/libdemos.so")
for _ in range(20000):
    x = lib.fib(60)
print(x)
```


## FFI: lib.rs

```
#[no_mangle]
pub extern fn fib(n: usize) -> u64 {
    let mut fibs = vec![1, 1];
    for pos in 0..cmp::max(n - 2, 0) {
        let newval = fibs[pos] + fibs[pos + 1];
        fibs.push(newval)
    }
    fibs[cmp::min(n - 1, fibs.len() - 1)]
}
```

note:
The no_mangle is needed to be C compatible; the extern to export the symbol in
the library.


## FFI: rust structs

```
#repr(C)
struct MyType {
    x: u64,
}
```


## RPC: Rust
```
impl Service for FibService {
    type Req = http::Message<http::Request>;
    type Resp = http::Message<http::Response>;
    type Error = http::Error;
    type Fut = BoxFuture<Self::Resp, http::Error>;

    fn call(&self, req: Self::Req) -> Self::Fut {
        let fib_req: FibRequest = serde_json::from_slice(req.body()).expect("json decode failed");
        let fib_resp = FibResponse { fib: fib(fib_req.n) };
        let resp = http::Message::new(http::Response::ok())
            .with_body(serde_json::to_vec(&fib_resp).expect("json encode failed"));
        finished(resp).boxed()
    }
}

pub fn main() {
    http::Server::new()
        .serve(|| FibService)
        .expect("server start failed");

    thread::sleep(Duration::from_secs(1_000_000));
}
```


## RPC: Python
```
import json

import requests

s = requests.Session()
for _ in range(200): # note 1% of the work of the in-process cases
    r = s.post('http://127.0.0.1:12345/', json = {'n': 60})
    x = (json.loads(r.text))['fib']
print(x)
```



## Results
```
$ trial.sh fib-iterator-60.pypy fib-cffi fib-json
+--------------------------------------------------+
|*                                                *|
|*                                                *|
|*                                                *|
|*                                                *|
|*                                                *|
|*                                                *|
|*                                                *|
|*                                                *|
|A                                                 |
|A                                                 |
|                                                 A|
+--------------------------------------------------+
    N           Min           Max        Median           Avg        Stddev
x  10          0.03          0.06          0.04         0.041  0.0073786479
+  10          0.03          0.03          0.03          0.03          -nan
Difference at 95.0% confidence
        -0.011 +/- 0.00490233
        -26.8293% +/- 11.9569%
        (Student's t, pooled s = 0.00521749)
*  10          8.07          8.12          8.08         8.086   0.019550504
Difference at 95.0% confidence
        8.045 +/- 0.0138836
        19622% +/- 33.8624%
        (Student's t, pooled s = 0.0147761)
```




## Questions?

Example code and these slides: 
https://github.com/rbtcollins/reveal.js/tree/master/kiwipycon-rust-2016/

* Robert Collins
* @rbtcollins
* lifeless on freenode
* rbtcollins@vmware.com
