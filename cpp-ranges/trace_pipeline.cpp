#include <iostream>
#include <vector>
#include <string>
#include <ranges>
#include <algorithm>

struct TraceEvent {
    int         timestamp;
    std::string signal_name;
    int         value;
    bool        is_bus_transaction;
};

// The ranges pipeline from Section 7: filter to bus transactions,
// filter to a time window, extract values, then delta consecutive pairs.
std::vector<int> deltas(const std::vector<TraceEvent>& trace,
                       int t_lo, int t_hi) {
    auto values_view = trace
        | std::views::filter([](const TraceEvent& e) {
              return e.is_bus_transaction;
          })
        | std::views::filter([&](const TraceEvent& e) {
              return e.timestamp >= t_lo && e.timestamp <= t_hi;
          })
        | std::views::transform([](const TraceEvent& e) {
              return e.value;
          });

    // One materialization. In C++23 this is: values_view | std::ranges::to<std::vector>()
    std::vector<int> values(values_view.begin(), values_view.end());

    std::vector<int> d;
    for (std::size_t i = 1; i < values.size(); ++i)
        d.push_back(values[i] - values[i - 1]);
    return d;
}

int main() {
    std::vector<TraceEvent> trace = {
        { 100, "clk",      0,  false },
        { 105, "data_bus", 42, true  },
        { 110, "clk",      1,  false },
        { 115, "data_bus", 47, true  },
        { 120, "irq",      1,  false },
        { 125, "data_bus", 51, true  },
        { 130, "data_bus", 158, true  },
        { 135, "clk",      0,  false },
    };

    const int t_lo = 112, t_hi = 132;

    // Show which values survive both filters, using the same pipeline.
    auto surviving = trace
        | std::views::filter([](const TraceEvent& e) { return e.is_bus_transaction; })
        | std::views::filter([&](const TraceEvent& e) {
              return e.timestamp >= t_lo && e.timestamp <= t_hi;
          })
        | std::views::transform([](const TraceEvent& e) { return e.value; });

    std::cout << "surviving bus values in [" << t_lo << ", " << t_hi << "]:";
    for (int v : surviving) std::cout << ' ' << v;
    std::cout << '\n';

    std::cout << "deltas:";
    for (int d : deltas(trace, t_lo, t_hi)) std::cout << ' ' << d;
    std::cout << '\n';

    return 0;
}