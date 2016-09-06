struct Baz;

impl Baz {
    fn foo(&mut self) {
        println!("foo")
    }
}

fn main() {
    let mut b = Baz {};
    let mut c = &mut b;
    let d = &mut c;
    c.foo();
    d.foo();
    b.foo();
}
