from pprint import pprint
from components import *
from solver import Circuit

# Example usage
circuit = Circuit()
circuit.add(VoltageSource(10, 'ground', 'node1'))
circuit.add(Resistor(10, 'node1', 'node2'))
circuit.add(Resistor(3, 'node2', 'ground'))
circuit.add(Resistor(5, 'node2', 'node3'))
# circuit.add(Diode('node3', 'ground'))
# circuit.add(Diode('ground', 'node3'))
circuit.add(Capacitor(1e-6, 'node3', 'ground', initial_voltage=0))

t_max = 0.001
time_step = 0.001

solver = circuit.get_solver(time_step)
final_voltages = solver.solve(t_max)

pprint(final_voltages)
