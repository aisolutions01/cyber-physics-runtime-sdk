"""
Runtime governance state machine.

Defines legal runtime transitions used by the
runtime governance layer.
"""

from enum import Enum


class RuntimeState(Enum):
    OBSERVE = "OBSERVE"
    ALERT = "ALERT"
    GOVERNANCE = "GOVERNANCE"
    STABILIZED = "STABILIZED"


class StateMachine:
    """
    Deterministic runtime state machine.
    """

    _ALLOWED_TRANSITIONS = {
        RuntimeState.OBSERVE: [RuntimeState.ALERT],
        RuntimeState.ALERT: [RuntimeState.GOVERNANCE],
        RuntimeState.GOVERNANCE: [RuntimeState.STABILIZED],
        RuntimeState.STABILIZED: [RuntimeState.OBSERVE],
    }

    def __init__(self):
        self._state = RuntimeState.OBSERVE

    @property
    def state(self) -> RuntimeState:
        return self._state

    def transition(self, next_state: RuntimeState) -> bool:
        """
        Perform a legal state transition.
        """
        allowed = self._ALLOWED_TRANSITIONS[self._state]

        if next_state not in allowed:
            return False

        self._state = next_state
        return True