from pprint import pprint
import numpy as np
from components import *

class Circuit:
	def __init__(self):
		self.resistors = []
		self.voltage_sources = []
		self.diodes = []
		self.capacitors = []
		self.nodes = set()

	def add_resistor(self, resistance, node1, node2):
		self.resistors.append(Resistor(resistance, node1, node2))
		self.nodes.update([node1, node2])
		self.update_node_index()

	def add_voltage_source(self, voltage, node1, node2):
		self.voltage_sources.append(VoltageSource(voltage, node1, node2))
		self.nodes.update([node1, node2])
		self.update_node_index()

	def add_capacitor(self, capacitance, node1, node2, initial_voltage=0):
		self.capacitors.append(Capacitor(capacitance, node1, node2, initial_voltage))
		self.nodes.update([node1, node2])
		self.update_node_index()

	def add_diode(self, node1, node2):
		self.diodes.append(Diode(node1, node2))
		self.nodes.update([node1, node2])
		self.update_node_index()

	def update_node_index(self):
		self.node_index = {node: index for index, node in enumerate(self.nodes)}

	def solve(self, time_step):
		# Initialize time variables
		time = 0
		voltages = {node: 0 for node in self.nodes}  # Initial voltages at nodes
		voltages['ground'] = 0  # Ground reference

		while True:  # Infinite loop until externally controlled
			# Build equations based on KCL for each node (except ground)
			A = np.zeros((len(self.nodes), len(self.nodes)))
			B = np.zeros(len(self.nodes))

			for node in self.nodes:
				if node == 'ground':
					continue

				node_eq_index = self.node_index[node]

				# Add equations for resistors and voltage sources...
				# (Assuming you have existing logic for resistors and voltage sources)

				for resistor in self.resistors:
					if resistor.node1 == node:
						other_node_index = self.node_index[resistor.node2]
						A[node_eq_index, node_eq_index] += 1 / resistor.resistance
						A[node_eq_index, other_node_index] -= 1 / resistor.resistance
					elif resistor.node2 == node:
						other_node_index = self.node_index[resistor.node1]
						A[node_eq_index, node_eq_index] += 1 / resistor.resistance
						A[node_eq_index, other_node_index] -= 1 / resistor.resistance

				for source in self.voltage_sources:
					if source.node1 == node:
						other_node_index = self.node_index[source.node2]
						A[node_eq_index, node_eq_index] += 1  # KVL for voltage source
						A[node_eq_index, other_node_index] -= 1  # KVL for voltage source
						B[node_eq_index] -= source.voltage
					elif source.node2 == node:
						other_node_index = self.node_index[source.node1]
						A[node_eq_index, node_eq_index] += 1  # KVL for voltage source
						A[node_eq_index, other_node_index] -= 1  # KVL for voltage source
						B[node_eq_index] += source.voltage

				for diode in self.diodes:
					if diode.node1 == node:  # Diode is forward biased
						other_node_index = self.node_index[diode.node2]
						A[node_eq_index, node_eq_index] += 1  # Current can flow
						A[node_eq_index, other_node_index] -= 1  # Current can flow
					elif diode.node2 == node:  # Diode is reverse biased
						other_node_index = self.node_index[diode.node1]
						# No changes to A or B since current cannot flow

				# Add equations for capacitors
				for capacitor in self.capacitors:
					if capacitor.node1 == node:
						other_node_index = self.node_index[capacitor.node2]
						dV_dt = (voltages[capacitor.node1] - voltages[capacitor.node2]) / time_step
						current = capacitor.capacitance * dV_dt
						A[node_eq_index, node_eq_index] += 1  # Current can flow
						A[node_eq_index, other_node_index] -= 1  # Current can flow
						B[node_eq_index] += current  # Add the current to the B matrix
					elif capacitor.node2 == node:
						other_node_index = self.node_index[capacitor.node1]
						dV_dt = (voltages[capacitor.node2] - voltages[capacitor.node1]) / time_step
						current = capacitor.capacitance * dV_dt
						A[node_eq_index, node_eq_index] += 1  # Current can flow
						A[node_eq_index, other_node_index] -= 1  # Current can flow
						B[node_eq_index] += current  # Add the current to the B matrix

			# Set ground node voltage to 0
			ground_index = self.node_index['ground']
			A[ground_index, :] = 0
			A[ground_index, ground_index] = 1
			B[ground_index] = 0

			# Enforce the voltage of the voltage sources
			for source in self.voltage_sources:
				if source.node1 == 'ground':
					node_eq_index = self.node_index[source.node2]
					A[node_eq_index, :] = 0  # Clear the equation for this node
					A[node_eq_index, node_eq_index] = 1  # Set the voltage at this node
					B[node_eq_index] = source.voltage  # Set the voltage to the source voltage
				elif source.node2 == 'ground':
					node_eq_index = self.node_index[source.node1]
					A[node_eq_index, :] = 0  # Clear the equation for this node
					A[node_eq_index, node_eq_index] = 1  # Set the voltage at this node
					B[node_eq_index] = -source.voltage  # Set the voltage to the source voltage (negative)


			# Solve the linear equations for the current time step
			voltages = dict(zip(self.nodes, np.linalg.solve(A, B).copy()))

			# Yield the current voltages
			yield voltages  # Return a copy of the voltages

			# Increment time
			time += time_step

# Example usage
circuit = Circuit()
circuit.add_voltage_source(10, 'ground', 'node1')
circuit.add_resistor(10, 'node1', 'node2')
circuit.add_resistor(3, 'node2', 'ground')
circuit.add_resistor(5, 'node2', 'node3')
# circuit.add_diode('node3', 'ground')
# circuit.add_diode('ground', 'node3')
circuit.add_capacitor(1e-6, 'node3', 'ground', initial_voltage=0)  # 1 μF capacitor

solver = circuit.solve(time_step=0.001)

for i in range(1000):
	final_voltages = solver.__next__()

pprint(final_voltages)

