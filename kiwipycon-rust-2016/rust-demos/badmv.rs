struct Baz;

impl Baz {
    fn foo(&self) {
        println!("foo")
    }
}

fn main() {
    let b = Baz {};
    let c = b;
    b.foo();
}
