// 03_indexed_iteration.cpp
// Index + element together, by zipping a range against iota.
// This is the pattern views::enumerate formalizes in C++23.
// Build: g++ -std=c++23 -O2 03_indexed_iteration.cpp -o indexed_iteration

#include <iostream>
#include <ranges>
#include <vector>
#include <string>
#include <format>
#include <map>

int main() {
    // ---------------------------------------------------------------
    // 1. Basic: enumerate signal names (hardware pin mapping)
    // ---------------------------------------------------------------
    std::vector<std::string> signals = { "clk", "data_bus", "irq", "reset" };

    std::cout << "=== Pin mapping ===\n";
    // zip pairs each element with its index from the infinite iota stream.
    for (auto [index, name] : std::views::zip(std::views::iota(0), signals))
        std::cout << std::format("  pin[{}] = {}\n", index, name);

    // ---------------------------------------------------------------
    // 2. Error reporting: parse a config file, show line numbers
    // ---------------------------------------------------------------
    std::vector<std::string> config_lines = {
        "timeout=30", "", "retries=3", "mode invalid", "port=8080"
    };

    std::cout << "\n=== Config validation ===\n";
    for (auto [line_no, line] : std::views::zip(std::views::iota(1), config_lines)) {
        if (line.empty()) {
            std::cout << std::format("  line {}: WARNING - empty line\n", line_no);
        } else if (line.find('=') == std::string::npos) {
            std::cout << std::format("  line {}: ERROR - missing '=' in '{}'\n", line_no, line);
        }
    }

    // ---------------------------------------------------------------
    // 3. Alternating row style: format a table with odd/even shading
    // ---------------------------------------------------------------
    std::vector<std::pair<std::string, int>> leaderboard = {
        {"Alice", 980}, {"Bob", 875}, {"Charlie", 810}, {"Diana", 790}
    };

    std::cout << "\n=== Leaderboard ===\n";
    for (auto [rank, entry] : std::views::zip(std::views::iota(1), leaderboard)) {
        // Odd/even rows get different markers (would be CSS classes in real UI)
        auto marker = (rank % 2 == 0) ? "  " : ">>";
        std::cout << std::format("  {} #{} {:10s} {:>5d} pts\n",
                                 marker, rank, entry.first, entry.second);
    }

    // ---------------------------------------------------------------
    // 4. Batch grouping: assign items to fixed-size batches
    // ---------------------------------------------------------------
    std::vector<std::string> items = {
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"
    };
    constexpr int batch_size = 3;

    std::cout << "\n=== Batch assignment ===\n";
    for (auto [idx, item] : std::views::zip(std::views::iota(0), items)) {
        std::cout << std::format("  batch {}: {}\n", idx / batch_size, item);
    }

    // ---------------------------------------------------------------
    // 5. C++23 views::enumerate - the cleaner spelling
    // ---------------------------------------------------------------
    std::cout << "\n=== C++23 enumerate ===\n";
    for (auto [i, name] : signals | std::views::enumerate)
        std::cout << std::format("  [{}] {}\n", i, name);

    return 0;
}