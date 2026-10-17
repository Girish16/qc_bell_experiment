"""Reproducible Bell-state experiment. Basis order |q1 q0> (Qiskit)."""
from __future__ import annotations
import numpy as np

BASIS = ("00", "01", "10", "11")
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
I = np.eye(2, dtype=complex)
# CNOT with control q0, target q1 in the basis |q1 q0>.
CNOT_0_1 = np.array([
    [1, 0, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0],
    [0, 1, 0, 0],
], dtype=complex)


def statevectors() -> dict[str, np.ndarray]:
    initial = np.array([1, 0, 0, 0], dtype=complex)
    after_h = np.kron(I, H) @ initial
    bell = CNOT_0_1 @ after_h
    return {"Initial": initial, "After H": after_h, "After CNOT": bell}


def probabilities() -> dict[str, np.ndarray]:
    return {stage: abs(state)**2 for stage, state in statevectors().items()}


def density_matrix(state: np.ndarray) -> np.ndarray:
    return np.outer(state, state.conjugate())


def classical_mixture() -> np.ndarray:
    """50/50 mixture of |00><00| and |11><11|."""
    return np.diag([.5, 0., 0., .5]).astype(complex)


def xx_expectation(rho: np.ndarray) -> float:
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    return float(np.trace(rho @ np.kron(X, X)).real)


if __name__ == "__main__":
    for stage, row in probabilities().items():
        print(stage, dict(zip(BASIS, row.round(3))))
