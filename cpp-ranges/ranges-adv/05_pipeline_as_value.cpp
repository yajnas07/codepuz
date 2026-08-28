// 05_pipeline_as_value.cpp
// A filter | transform chain stored in a variable and reused across inputs.
// Pipelines are values: "ranges as vocabulary" made concrete.
// Requires C++23 (std::ranges::to): g++ -std=c++23 -O2 05_pipeline_as_value.cpp -o pipeline_as_value

#include <iostream>
#include <ranges>
#include <vector>
#include <string>
#include <format>
#include <cctype>

int main() {
    // A reusable adaptor object: keep the even numbers, square them.
    // This is a composed adaptor - it holds no data, only the recipe.
    // filter(pred) | transform(fn) produces a single pipeline object
    // that can be applied to any range later with the pipe operator.
    auto even_squares = std::views::filter([](int n) { return n % 2 == 0; })
                      | std::views::transform([](int n) { return n * n; });

    std::vector<int> a = { 1, 2, 3, 4, 5, 6 };
    std::vector<int> b = { 10, 15, 20, 25 };

    // Apply the same pipeline to two different inputs.
    // "a | even_squares" binds the recipe to vector a, producing a lazy view.
    // std::ranges::to<std::vector>() materializes the lazy view into an
    // actual vector - this is the point where computation happens.
    // The pipeline itself is stateless and can be reused on any input.
    auto from_a = a | even_squares | std::ranges::to<std::vector>();
    auto from_b = b | even_squares | std::ranges::to<std::vector>();

    std::cout << "from a:";
    for (int x : from_a) std::cout << ' ' << x;
    std::cout << "\nfrom b:";
    for (int x : from_b) std::cout << ' ' << x;
    std::cout << '\n';

    // expected:
    // from a: 4 16 36
    // from b: 100 400

    // ---------------------------------------------------------------
    // 2. Log sanitizer: a reusable text-cleaning pipeline
    // ---------------------------------------------------------------
    // Real-world scenario: The received log lines from multiple sources
    // and need to normalize them before indexing — strip blank lines,
    // trim whitespace, and convert to lowercase.

    // Pipeline: drop empty lines → trim leading/trailing spaces → lowercase
    auto clean_line = [](std::string s) {
        // trim leading spaces
        auto start = s.find_first_not_of(" \t");
        if (start == std::string::npos) return std::string{};
        s = s.substr(start);
        // trim trailing spaces
        auto end = s.find_last_not_of(" \t");
        s = s.substr(0, end + 1);
        // lowercase
        for (auto& c : s) c = static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
        return s;
    };

    auto sanitize = std::views::filter([](const std::string& s) { return !s.empty(); })
                  | std::views::transform(clean_line)
                  | std::views::filter([](const std::string& s) { return !s.empty(); });

    // Compose a stricter pipeline: sanitize + keep only critical errors
    auto critical_only = sanitize
                       | std::views::filter([](const std::string& s) {
                             return s.starts_with("error") || s.starts_with("critical");
                         });

    std::vector<std::string> server_logs = {
        "  ERROR: Disk full  ", "", "  Warning: Retry #3", "   ",
        "INFO: Connection OK", "", "  DEBUG: cache miss  "
    };

    std::vector<std::string> app_logs = {
        "", "  CRITICAL: OOM  ", "  info: request served", "TRACE: heartbeat"
    };

    // Same pipeline, two different log sources
    auto clean_server = server_logs | sanitize | std::ranges::to<std::vector>();
    auto clean_app    = app_logs    | sanitize | std::ranges::to<std::vector>();

    std::cout << "\nserver logs (cleaned):\n";
    for (auto& l : clean_server) std::cout << "  [" << l << "]\n";

    std::cout << "app logs (cleaned):\n";
    for (auto& l : clean_app) std::cout << "  [" << l << "]\n";

    // critical_only builds on sanitize — pipelines compose with each other.
    // After lowercasing, we match lines starting with "error" or "critical".
    auto server_critical = server_logs | critical_only | std::ranges::to<std::vector>();
    auto app_critical    = app_logs    | critical_only | std::ranges::to<std::vector>();

    std::cout << "\nserver critical errors:\n";
    for (auto& l : server_critical) std::cout << "  [" << l << "]\n";

    std::cout << "app critical errors:\n";
    for (auto& l : app_critical) std::cout << "  [" << l << "]\n";


    return 0;
}