#![feature(custom_derive, plugin)]
#![plugin(serde_macros)]
extern crate serde;
extern crate serde_json;
extern crate tokio_service;
#[macro_use]
extern crate hyper;
extern crate tokio_hyper as http;
extern crate futures;

use tokio_service::Service;
use futures::{BoxFuture, finished, Future};
use std::cmp;
use std::io;
use std::thread;
use std::time::Duration;

#[derive(Debug, PartialEq, Serialize, Deserialize)]
struct FibRequest {
    pub n: usize,
}

#[derive(Debug, PartialEq, Serialize, Deserialize)]
struct FibResponse {
    fib: u64,
}

#[derive(Clone)]
struct FibService;

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

fn fib(n: usize) -> u64 {
    let mut fibs = vec![1, 1];
    for pos in 0..cmp::max(n - 2, 0) {
        let newval = fibs[pos] + fibs[pos + 1];
        fibs.push(newval)
    }
    fibs[cmp::min(n - 1, fibs.len() - 1)]
}

pub fn main() {
    http::Server::new()
        .serve(|| FibService)
        .expect("server start failed");

    thread::sleep(Duration::from_secs(1_000_000));
}
