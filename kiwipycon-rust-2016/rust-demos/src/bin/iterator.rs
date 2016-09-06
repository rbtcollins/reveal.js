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
