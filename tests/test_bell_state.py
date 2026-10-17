"""Seven checks for amplitudes, Z probabilities and X correlations."""
import unittest
import numpy as np
from src.bell_state import (
    BASIS, statevectors, probabilities, density_matrix,
    classical_mixture, xx_expectation,
)


class BellStateTests(unittest.TestCase):
    def test_basis_order(self):
        self.assertEqual(BASIS, ("00", "01", "10", "11"))

    def test_normalization(self):
        for state in statevectors().values():
            self.assertAlmostEqual(float(np.vdot(state, state).real), 1.)

    def test_hadamard_on_q0(self):
        np.testing.assert_allclose(
            statevectors()["After H"], [1/np.sqrt(2), 1/np.sqrt(2), 0, 0], atol=1e-12)

    def test_cnot_bell_state(self):
        np.testing.assert_allclose(
            statevectors()["After CNOT"], [1/np.sqrt(2), 0, 0, 1/np.sqrt(2)], atol=1e-12)

    def test_z_probabilities(self):
        for label, expected in zip(probabilities(), (
            [1, 0, 0, 0], [.5, .5, 0, 0], [.5, 0, 0, .5]
        )):
            np.testing.assert_allclose(probabilities()[label], expected, atol=1e-12)

    def test_same_z_histogram_for_classical_mixture(self):
        bell = density_matrix(statevectors()["After CNOT"])
        np.testing.assert_allclose(
            np.diag(bell).real, np.diag(classical_mixture()).real, atol=1e-12)

    def test_xx_distinguishes_bell_and_classical_mixture(self):
        self.assertAlmostEqual(xx_expectation(density_matrix(statevectors()["After CNOT"])), 1.)
        self.assertAlmostEqual(xx_expectation(classical_mixture()), 0.)


if __name__ == "__main__":
    unittest.main()
