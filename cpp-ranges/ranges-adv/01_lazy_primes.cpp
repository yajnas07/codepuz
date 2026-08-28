// 01_lazy_primes.cpp
// Lazy infinite sequences: an unbounded stream, filtered and capped.
// Build: g++ -std=c++20 -O2 01_lazy_primes.cpp -o lazy_primes
// Usage: ./lazy_primes [start] [count]
//   start — beginning of the integer stream (default: 2)
//   count — how many primes to collect     (default: 100)

#include <cstdlib>
#include <iostream>
#include <ranges>

static unsigned int call_count = 0;
bool is_prime(int n) {
     ++call_count;
    if (n < 2) return false;
    for (int d = 2; d * 1LL * d <= n; ++d)
        if (n % d == 0) return false;
    return true;
}

int main(int argc, char* argv[]) {
    int start = (argc > 1) ? std::atoi(argv[1]) : 2;
    int count = (argc > 2) ? std::atoi(argv[2]) : 100;

    // views::iota(start) is infinite: start, start+1, start+2, ...
    // Nothing is computed until take pulls exactly `count` primes out the far end.
    auto primes = std::views::iota(start)
        | std::views::filter(is_prime)
        | std::views::take(count);

    std::cout << count << " primes starting from " << start << ":";
    for (int p : primes)
        std::cout << ' ' << p;
    std::cout << '\n';

    std::cout << "is_prime was called " << call_count << " times\n";

    return 0;
}