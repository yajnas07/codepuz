// derivative_trend.cpp
//
// CodePuz - "The Derivative That Saw It Coming"
// https://codepuz.com
//
// A minimal, self-contained demonstration of numerical first and second
// derivatives applied to a stream of metric samples. The goal is to show
// how the second derivative flags a trend (accelerating, plateauing, or
// regressing) before the value itself makes the change obvious.
//
// Compile:
//   g++ -std=c++17 -O2 -o derivative_trend derivative_trend.cpp
//
// Run:
//   ./derivative_trend

#include <iostream>
#include <iomanip>
#include <vector>
#include <string>
#include <cmath>
#include <cassert>
#include <functional>

// ============================================================
// Core types
// ============================================================

struct Sample {
    double time;
    double value;
};

// Result of analysing one sample in the stream. First and second derivatives
// are computed via simple finite differences; a human-readable trend label is
// derived from the sign and magnitude of the second derivative.
struct TrendResult {
    double time;
    double value;
    double first_deriv;   // rate of change
    double second_deriv;  // rate of the rate
    std::string trend;    // "ACCELERATING" | "PLATEAUING" | "REGRESSING"
    bool flagged;         // true if the second derivative crosses the threshold
};

// ============================================================
// Numerical derivative engine
// ============================================================
//
// Uses a simple finite-difference scheme: at each step we have access to the
// current and previous samples, so we can compute first and second derivatives
// without buffering the entire stream.
//
// d1[n]  = (v[n]  - v[n-1]) / dt       -- forward difference, 1st derivative
// d2[n]  = (d1[n] - d1[n-1]) / dt      -- forward difference of d1, 2nd deriv
//
// This is deliberately kept simple: the point of the post is the concept, not
// production-grade numerical methods. For real signal processing you would use
// a Savitzky-Golay filter or similar; see the closing note in the post.

class DerivativeStream {
public:
    explicit DerivativeStream(double accel_threshold = 0.01)
        : accel_threshold_(accel_threshold)
        , has_prev_(false)
        , has_prev_d1_(false)
    {}

    // Feed one sample into the stream. Returns a populated TrendResult once
    // at least two consecutive samples have been seen (needed for d1), and a
    // populated second_deriv once three samples have been seen (needed for d2).
    // Before enough samples are available the derivatives are zero.
    TrendResult push(const Sample& s) {
        TrendResult result{};
        result.time  = s.time;
        result.value = s.value;
        result.trend = "WAITING";
        result.flagged = false;

        if (!has_prev_) {
            prev_ = s;
            has_prev_ = true;
            return result;
        }

        double dt = s.time - prev_.time;
        if (dt <= 0.0) {
            prev_ = s;
            return result;
        }

        double d1 = (s.value - prev_.value) / dt;
        result.first_deriv = d1;

        if (has_prev_d1_) {
            double d2 = (d1 - prev_d1_) / dt;
            result.second_deriv = d2;
            result.trend = classify(d2);
            result.flagged = std::abs(d2) > accel_threshold_;
        } else {
            result.trend = "WAITING";
        }

        prev_     = s;
        prev_d1_  = d1;
        has_prev_d1_ = true;

        return result;
    }

    void reset() {
        has_prev_    = false;
        has_prev_d1_ = false;
    }

private:
    std::string classify(double d2) const {
        if (d2 >  accel_threshold_) return "ACCELERATING";
        if (d2 < -accel_threshold_) return "REGRESSING";
        return "PLATEAUING";
    }

    double  accel_threshold_;
    Sample  prev_{};
    double  prev_d1_{};
    bool    has_prev_;
    bool    has_prev_d1_;
};

// ============================================================
// Pretty-printer
// ============================================================

void print_header() {
    std::cout
        << std::left
        << std::setw(7)  << "time"
        << std::setw(10) << "value"
        << std::setw(10) << "f'(t)"
        << std::setw(12) << "f''(t)"
        << std::setw(16) << "trend"
        << "flag\n"
        << std::string(60, '-') << "\n";
}

void print_result(const TrendResult& r) {
    if (r.trend == "WAITING") {
        std::cout
            << std::left  << std::setw(7)  << std::fixed << std::setprecision(1) << r.time
            << std::setw(10) << std::setprecision(4) << r.value
            << "\n";
        return;
    }
    std::cout
        << std::left
        << std::setw(7)  << std::fixed << std::setprecision(1) << r.time
        << std::setw(10) << std::setprecision(4) << r.value
        << std::setw(10) << std::showpos << r.first_deriv
        << std::setw(12) << r.second_deriv
        << std::noshowpos
        << std::setw(16) << r.trend
        << (r.flagged ? "***" : "")
        << "\n";
}

// ============================================================
// Test helpers
// ============================================================

void run_stream(
    const std::string& label,
    const std::vector<Sample>& samples,
    double threshold = 0.01)
{
    std::cout << "\n=== " << label << " ===\n";
    print_header();
    DerivativeStream ds(threshold);
    for (const auto& s : samples) {
        print_result(ds.push(s));
    }
}

// Generate a logistic (S-curve) stream - same curve as the blog widgets.
// This mimics a metric that starts slow, accelerates, then plateaus.
std::vector<Sample> logistic_stream(int n = 20, double k = 1.2) {
    std::vector<Sample> out;
    for (int i = 0; i < n; i++) {
        double t = -5.0 + 10.0 * i / (n - 1);
        double v = 1.0 / (1.0 + std::exp(-k * t));
        out.push_back({t, v});
    }
    return out;
}

// Generate a steadily accelerating stream (parabola) - value rises but the
// rate of change itself is also growing, second derivative stays positive.
std::vector<Sample> accelerating_stream(int n = 15) {
    std::vector<Sample> out;
    for (int i = 0; i < n; i++) {
        double t = i * 1.0;
        double v = 0.05 * t * t;
        out.push_back({t, v});
    }
    return out;
}

// Generate a plateauing stream - value still grows but the rate is falling.
std::vector<Sample> plateauing_stream(int n = 15) {
    std::vector<Sample> out;
    for (int i = 0; i < n; i++) {
        double t = i * 1.0;
        double v = std::sqrt(t + 0.1) * 2.0;
        out.push_back({t, v});
    }
    return out;
}

// Generate a regressing stream - value was rising but now trending down;
// second derivative turns negative before the value itself drops.
std::vector<Sample> regressing_stream(int n = 15) {
    std::vector<Sample> out;
    for (int i = 0; i < n; i++) {
        double t = i * 1.0;
        // linear rise then quadratic fall
        double v = (t < 6.0)
            ? 0.4 * t
            : 2.4 - 0.08 * (t - 6.0) * (t - 6.0);
        out.push_back({t, v});
    }
    return out;
}

// Noisy stream: linear trend buried under random-ish noise.
// The second derivative fluctuates but trends slightly positive throughout.
std::vector<Sample> noisy_stream(int n = 20) {
    std::vector<Sample> out;
    // Deterministic "noise" so the output is reproducible without <random>
    const double noise[] = {
        0.00,  0.03, -0.02,  0.05, -0.01,  0.04, -0.03,  0.06,
       -0.02,  0.03,  0.01, -0.04,  0.05, -0.01,  0.02, -0.03,
        0.04,  0.00, -0.02,  0.05
    };
    for (int i = 0; i < n; i++) {
        double t = i * 1.0;
        double v = 0.1 * t + noise[i % 20];
        out.push_back({t, v});
    }
    return out;
}

// ============================================================
// Simple assertion helpers for compile-time-verifiable output
// ============================================================

void test_single_sample_gives_waiting() {
    DerivativeStream ds;
    auto r = ds.push({0.0, 1.0});
    assert(r.trend == "WAITING");
    std::cout << "[PASS] single sample => WAITING\n";
}

void test_two_samples_give_d1_but_no_d2() {
    DerivativeStream ds;
    ds.push({0.0, 0.0});
    auto r = ds.push({1.0, 1.0});
    assert(std::abs(r.first_deriv - 1.0) < 1e-9);
    assert(r.trend == "WAITING");
    std::cout << "[PASS] two samples => d1=1.0, trend=WAITING\n";
}

void test_three_samples_accelerating() {
    // v = t^2: d1 = 2t, d2 = 2 (constant acceleration)
    DerivativeStream ds(0.01);
    ds.push({0.0, 0.0});
    ds.push({1.0, 1.0});
    auto r = ds.push({2.0, 4.0});
    assert(r.trend == "ACCELERATING");
    assert(r.flagged == true);
    std::cout << "[PASS] parabola => ACCELERATING, flagged=true\n";
}

void test_plateau_detection() {
    // sqrt grows but decelerates: d2 negative, should REGRESS or PLATEAU
    DerivativeStream ds(0.01);
    ds.push({0.0, 0.0});
    ds.push({1.0, 1.0});
    ds.push({4.0, 2.0});
    auto r = ds.push({9.0, 3.0});
    // d1[1] = 1/1 = 1, d1[2] = 1/3, d1[3] = 1/5, d2 < 0
    assert(r.trend == "REGRESSING" || r.trend == "PLATEAUING");
    std::cout << "[PASS] sqrt curve => REGRESSING/PLATEAUING (decelerating)\n";
}

void test_reset_clears_state() {
    DerivativeStream ds;
    ds.push({0.0, 1.0});
    ds.push({1.0, 2.0});
    ds.reset();
    auto r = ds.push({2.0, 3.0});
    assert(r.trend == "WAITING");
    std::cout << "[PASS] reset() clears state => next push gives WAITING\n";
}

// ============================================================
// main
// ============================================================

int main() {
    std::cout << "=== Unit tests ===\n";
    test_single_sample_gives_waiting();
    test_two_samples_give_d1_but_no_d2();
    test_three_samples_accelerating();
    test_plateau_detection();
    test_reset_clears_state();

    // --- Stream demonstrations ---
    // Each stream mimics a different real-world metric behaviour.
    // The "***" flag lights up when |f''(t)| crosses the threshold,
    // signalling a trend shift before the value itself makes it visible.

    run_stream("Logistic / S-curve (slow start, fast middle, plateau)",
               logistic_stream(), 0.005);

    run_stream("Steadily accelerating (parabola)",
               accelerating_stream(), 0.01);

    run_stream("Plateauing (sqrt growth - rate is falling)",
               plateauing_stream(), 0.01);

    run_stream("Regressing (rises then bends down)",
               regressing_stream(), 0.01);

    run_stream("Noisy linear trend",
               noisy_stream(), 0.02);

    return 0;
}