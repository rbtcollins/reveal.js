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
