"""
Runtime entropy measurement primitives.

This module evaluates simple instability indicators
from telemetry observations.
"""

from statistics import variance
from typing import List


class EntropyEngine:
    """
    Computes runtime instability metrics.
    """

    def compute(self, values: List[float]) -> dict:
        """
        Calculate entropy-related metrics.

        Returns:
            {
                "entropy": float,
                "variance": float,
                "jitter": float
            }
        """
        if len(values) < 2:
            return {
                "entropy": 0.0,
                "variance": 0.0,
                "jitter": 0.0,
            }

        value_variance = variance(values)

        jitter = sum(
            abs(values[i] - values[i - 1])
            for i in range(1, len(values))
        ) / (len(values) - 1)

        entropy = value_variance + jitter

        return {
            "entropy": round(entropy, 6),
            "variance": round(value_variance, 6),
            "jitter": round(jitter, 6),
        }