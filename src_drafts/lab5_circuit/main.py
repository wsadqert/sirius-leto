from rich.traceback import install
from pprint import pprint

from components import *
from solver import Circuit
from units import u

install(show_locals=True, width=300)

# # Example usage
# circuit = Circuit()
# circuit.add(VoltageSource(10, 'ground', 'node1'))
# circuit.add(Resistor(10, 'node1', 'node2'))
# circuit.add(Resistor(3, 'node2', 'ground'))
# circuit.add(Resistor(5, 'node2', 'node3'))
# # circuit.add(Diode('node3', 'ground'))
# # circuit.add(Diode('ground', 'node3'))
# circuit.add(Capacitor(1e-6, 'node3', 'ground', initial_voltage=0))

# voltmeter = Voltmeter("node1", "node3")
# circuit.add(voltmeter)

# ammeter = Ammeter("node2", "node3")
# circuit.add(ammeter)

# t_max = 0.001
# time_step = 0.001

# solver = circuit.get_solver(time_step)
# final_voltages = solver.solve(t_max)

# pprint(final_voltages)

# print(voltmeter.get_value())
# print(ammeter.get_value())

# Example usage
circuit = Circuit()

circuit.set_instrumental_precise(1e-5)

v1 = VoltageSource(5, 'ground', 'node1')
ammeter = Ammeter("node1", "node2")
c1 = Capacitor(15 * u.micro, 'node2', 'node3')
# circuit.add(Capacitor(1e-6, "node2", "node3"))
r1 = Resistor(100, 'node3', 'ground')
voltmeter = Voltmeter("node2", "node3")

circuit.add([v1, c1, r1])
circuit.add(ammeter)
circuit.add(voltmeter)

t_max = 2 * u.milli
time_step = 5 * u.micro

solver = circuit.get_solver(time_step)
final_voltages = solver.solve(t_max)

print()

print("v =", voltmeter.get_value())
print("a =", ammeter.get_value())
