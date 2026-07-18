# Derivative Trends

`derivative-trends.cpp` is a small streaming demonstration of how numerical
derivatives can reveal a change in a metric's direction before that change is
obvious from the metric value alone.

For every timestamped value, it calculates the first derivative (the current
rate of change) and then the second derivative (whether that rate is speeding
up or slowing down). It labels the result as `ACCELERATING`, `PLATEAUING`, or
`REGRESSING`, and flags changes whose second derivative exceeds a configurable
threshold.

The example includes several synthetic streams—an S-curve, steady
acceleration, a plateau, a decline, and noisy data—to show both the usefulness
of this signal and its sensitivity to noise. It keeps only the previous sample
and previous rate, making it suitable as a simple real-time or monitoring
example rather than a production-grade forecasting system.

> Note: `REGRESSING` here means the growth rate is decreasing; the metric may
> still be increasing.
