"""
Runtime governance coordinator.

Coordinates runtime state transitions using
entropy and CFL boundary measurements.
"""

from sdk.state_machine import RuntimeState
from sdk.state_machine import StateMachine

class RuntimeGovernance:
    """
    Deterministic runtime governance controller.
    """

    ENTROPY_ALERT = 0.20
    ENTROPY_GOV = 0.40
    CFL_GOV = 0.60

    def __init__(self,state_machine: StateMachine):
        self.state_machine = state_machine

    def step(self, entropy: float, cfl: float) -> RuntimeState:
        """
        Evaluate governance conditions and perform
        state transitions when required.
        """

        current = self.state_machine.state

        if (
            current == RuntimeState.OBSERVE
            and entropy > self.ENTROPY_ALERT
        ):
            self.state_machine.transition(RuntimeState.ALERT)

        elif (
            current == RuntimeState.ALERT
            and entropy > self.ENTROPY_GOV
            and cfl > self.CFL_GOV
        ):
            self.state_machine.transition(
                RuntimeState.GOVERNANCE
            )

        elif (
            current == RuntimeState.GOVERNANCE
            and entropy < self.ENTROPY_ALERT
            and cfl < self.CFL_GOV
        ):
            self.state_machine.transition(
                RuntimeState.STABILIZED
            )

        return self.state_machine.state