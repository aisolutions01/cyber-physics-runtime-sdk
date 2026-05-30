"""
Canonical runtime governance example.

This example demonstrates the minimal Cyber-Physics
runtime stabilization flow using the SDK primitives.

Flow:

Telemetry
    ↓
Entropy Evaluation
    ↓
CFL Boundary Evaluation
    ↓
Governance Decision
    ↓
State Transition
"""

from sdk.telemetry import TelemetryBuffer
from sdk.entropy import EntropyEngine
from sdk.cfl import CFLMonitor
from sdk.state_machine import StateMachine
from sdk.runtime_governance import RuntimeGovernance


def main():
    """
    Execute a simple runtime governance cycle.
    """

    telemetry = TelemetryBuffer(max_events=20)

    entropy_engine = EntropyEngine()
    cfl_monitor = CFLMonitor()

    state_machine = StateMachine()

    governance = RuntimeGovernance(
        state_machine=state_machine
    )

    # Simulated telemetry observations.
    runtime_values = [
        0.05,
        0.95,
        0.10,
        0.90,
        0.15,
        1.00,
        0.05,
        0.98,
        0.12,
        0.93,
    ]

    # Feed telemetry into the observation layer.
    for value in runtime_values:
        telemetry.ingest(
            {
                "metric": value
            }
        )

    # Extract telemetry values.
    values = [
        event["metric"]
        for event in telemetry.get_events()
    ]

    # Measure runtime instability.
    entropy_metrics = entropy_engine.compute(values)

    entropy = entropy_metrics["entropy"]

    # Evaluate CFL boundary conditions.
    cfl_metrics = cfl_monitor.evaluate(entropy)

    cfl = cfl_metrics["cfl"]

    # Execute governance cycles.
    state_before = state_machine.state

    for _ in range(3):
        state_after = governance.step(
            entropy=entropy,
            cfl=cfl
        )

    print("\n=== Cyber-Physics Runtime SDK ===\n")

    print(f"Initial State : {state_before.value}")

    print(
        f"Entropy       : "
        f"{entropy_metrics['entropy']}"
    )

    print(
        f"Variance      : "
        f"{entropy_metrics['variance']}"
    )

    print(
        f"Jitter        : "
        f"{entropy_metrics['jitter']}"
    )

    print(
        f"CFL           : "
        f"{cfl_metrics['cfl']}"
    )

    print(
        f"Margin        : "
        f"{cfl_metrics['margin']}"
    )

    print(
        f"Pressure      : "
        f"{cfl_metrics['pressure']}"
    )

    print(
        f"Final State   : "
        f"{state_after.value}"
    )

    print("\nRuntime cycle completed.\n")


if __name__ == "__main__":
    main()
