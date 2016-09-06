struct Baz;

impl Baz {
    fn foo(&mut self) {
        println!("foo")
    }
}

fn main() {
    let mut b = Baz {};
    let c = &mut b;
    b.foo();
}
