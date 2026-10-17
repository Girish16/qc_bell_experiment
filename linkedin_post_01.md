# LinkedIn post 01 — From two qubits to entanglement

Two bars. Both at 50%.

That's what the computational-basis measurement probabilities of a Bell state look like. But those bars don't tell the whole story.

I've been building a small set of quantum-computing visualizations in Python. I started with a two-qubit circuit: Hadamard on q0, followed by CNOT.

The final state is (|00⟩ + |11⟩)/√2. A measurement gives 00 or 11 with equal probability.

The interesting part: a classical mixture can produce the *same* histogram. Those measurement probabilities alone don't establish entanglement.

Next, I'm exploring what changes when we compare density matrices and measurements in another basis.

Code and reproducible figures: https://github.com/Girish16/qc_bell_experiment

#QuantumComputing #Python #QuantumInformation #DataVisualization

Note: basis kets use Qiskit's |q1 q0⟩ bit order.
