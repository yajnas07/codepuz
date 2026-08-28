// 04_moving_average.cpp
// Windowed processing with views::slide — a C++23 view that produces
// overlapping sub-ranges of N consecutive elements from any range.
// Requires C++23: g++ -std=c++23 -O2 04_moving_average.cpp -o moving_average

#include <iostream>
#include <ranges>
#include <vector>
#include <numeric>
#include <algorithm>
#include <format>

int main() {
    // ---------------------------------------------------------------
    // 1. Moving average: smooth noisy signal data
    // ---------------------------------------------------------------
    std::vector<int> samples = { 10, 12, 14, 20, 22, 18 };
    constexpr int window_size = 3;

    // slide(3) produces a lazy view of overlapping windows:
    //   window 0: {10, 12, 14}
    //   window 1: {12, 14, 20}
    //   window 2: {14, 20, 22}
    //   window 3: {20, 22, 18}
    // No data is copied — each window is a subrange into the original vector.
    //
    // transform then computes the average of each window lazily.
    // std::accumulate sums the elements; dividing by window_size (as double)
    // gives the mean. Nothing runs until we iterate over moving_avg below.
    auto moving_avg = samples
        | std::views::slide(window_size)
        | std::views::transform([](auto window) {
              int sum = std::accumulate(window.begin(), window.end(), 0);
              return sum / 3.0;
          });

    std::cout << "3-point moving average:";
    for (double a : moving_avg)
        std::cout << std::format(" {:.2f}", a);
    std::cout << '\n';
    // Output: 12.00 15.33 18.67 20.00

    // ---------------------------------------------------------------
    // 2. Detect consecutive spikes: find any window where all values
    //    exceed a threshold (e.g. sustained high CPU usage)
    // ---------------------------------------------------------------
    std::vector<int> cpu_usage = { 40, 55, 92, 95, 88, 30, 91, 97, 93, 45 };
    constexpr int spike_window = 3;
    constexpr int threshold = 85;

    // slide(3) lets us inspect every group of 3 consecutive readings.
    // We check if ALL values in a window exceed the threshold — that
    // indicates a sustained spike, not just a momentary blip.
    std::cout << "\nCPU readings: ";
    for (int v : cpu_usage) std::cout << v << ' ';
    std::cout << '\n';

    int window_idx = 0;
    for (auto window : cpu_usage | std::views::slide(spike_window)) {
        bool all_high = std::ranges::all_of(window,
                            [&](int v) { return v > threshold; });
        if (all_high) {
            std::cout << std::format("  SPIKE at index {}: ", window_idx);
            for (int v : window) std::cout << v << ' ';
            std::cout << '\n';
        }
        ++window_idx;
    }
    // Output:
    //   SPIKE at index 2: 92 95 88
    //   SPIKE at index 6: 91 97 93

    return 0;
}