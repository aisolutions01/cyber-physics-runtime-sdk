"""
Telemetry ingestion primitives.

This module provides a lightweight telemetry buffer used
for runtime observation experiments.
"""

from collections import deque
from typing import Any, Dict, List


class TelemetryBuffer:
    """
    Stores recent telemetry events in a bounded buffer.
    """

    def __init__(self, max_events: int = 100):
        self._events = deque(maxlen=max_events)

    def ingest(self, event: Dict[str, Any]) -> None:
        """
        Add a telemetry event to the buffer.
        """
        self._events.append(event)

    def get_events(self) -> List[Dict[str, Any]]:
        """
        Return buffered telemetry events.
        """
        return list(self._events)

    def clear(self) -> None:
        """
        Clear all buffered events.
        """
        self._events.clear()