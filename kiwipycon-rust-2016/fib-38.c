#include <stdio.h>
#include <stdint.h>

uint64_t fib(int64_t n) {
    if (n <= 2) {
        return 1;
    } else {
        return fib(n - 1) + fib(n - 2);
    }
}

void main() {
    printf("%lu\n", fib(38));
}
