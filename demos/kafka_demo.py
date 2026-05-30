"""
Kafka-style telemetry propagation demonstration.

This example simulates a distributed telemetry stream
flowing through the Cyber-Physics Runtime SDK.

The demonstration does not require a real Kafka cluster.

Flow:

Telemetry Stream
    ↓
Entropy Evaluation
    ↓
CFL Boundary Evaluation
    ↓
Governance Transition
"""

import random
import time

from sdk.telemetry import TelemetryBuffer
from sdk.entropy import EntropyEngine
from sdk.cfl import CFLMonitor
from sdk.state_machine import StateMachine
from sdk.runtime_governance import RuntimeGovernance

DEMO_DELAY = 0.25

def generate_telemetry_value(step: int) -> float:
    """
    Generate simulated telemetry values.

    The simulation introduces a temporary propagation burst
    to demonstrate governance activation behavior.
    """

    if 8 <= step <= 14:
        return random.uniform(0.75, 1.00)

    return random.uniform(0.05, 0.30)


def main():
    """
    Execute a Kafka-style telemetry propagation simulation.
    """

    telemetry = TelemetryBuffer(max_events=25)

    entropy_engine = EntropyEngine()
    cfl_monitor = CFLMonitor()

    state_machine = StateMachine()

    governance = RuntimeGovernance(
        state_machine=state_machine
    )

    print("\n=== Kafka Telemetry Demonstration ===\n")

    for step in range(20):

        telemetry_value = generate_telemetry_value(step)

        telemetry.ingest(
            {
                "metric": telemetry_value
            }
        )

        values = [
            event["metric"]
            for event in telemetry.get_events()
        ]

        entropy_metrics = entropy_engine.compute(values)

        entropy = entropy_metrics["entropy"]

        cfl_metrics = cfl_monitor.evaluate(entropy)

        cfl = cfl_metrics["cfl"]

        state = governance.step(
            entropy=entropy,
            cfl=cfl
        )

        print(
            f"[Step {step:02d}] "
            f"Metric={telemetry_value:.3f} "
            f"Entropy={entropy:.3f} "
            f"CFL={cfl:.3f} "
            f"State={state.value}"
        )

        time.sleep(DEMO_DELAY)

    print("\nSimulation completed.\n")


if __name__ == "__main__":
    main()
