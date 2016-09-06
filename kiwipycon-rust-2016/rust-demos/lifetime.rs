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
