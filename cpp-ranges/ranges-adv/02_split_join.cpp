// 02_split_join.cpp
// String processing with views::split and views::join, no index arithmetic.
// Build: g++ -std=c++20 -O2 02_split_join.cpp -o split_join

#include <iostream>
#include <vector>
#include <ranges>
#include <string>
#include <string_view>

int main() {
    std::string line = "The quick brown fox jumps over 13 lazy dogs. On 2026-08-28, Alice sent an email to bob@example.com with the subject: \"Test #42: Parsing Strings\". The message contained numbers (12345, -67.89, 0xFF), symbols (@, #, $, %, &, *), and escaped characters such as \\n, \\t, and \\\\";

    std::vector<std::string> tokens;
    // Split on commas. Each piece is itself a lazy subrange of chars
    // no new strings are created by the split itself.
    // We convert each subrange to a string_view for printing, then
    // store a copy in the tokens vector for the join step later.
    std::cout << "fields:\n";
    for (auto field : line | std::views::split(',')) {
        std::string_view sv(field.begin(), field.end());
        std::cout << "  [" << sv << "]\n";
        tokens.push_back(std::string(sv));
    }

    // Join a set of tokens back together with a separator.
    // join_with flattens the vector of strings into a single lazy character
    // sequence, inserting " | " between each element — no allocation needed.
    // It is the C++23 equivalent of Python's " | ".join(tokens).
    std::cout << "joined back with (|): ";
    for (auto c : tokens | std::views::join_with(std::string(" | ")))
        std::cout << c;
    std::cout << '\n';

    return 0;
}