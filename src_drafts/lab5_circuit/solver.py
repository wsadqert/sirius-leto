import numpy as np
from tqdm import tqdm
from components import *

class Circuit:
	def __init__(self):
		self.resistors = []
		self.voltage_sources = []
		self.diodes = []
		self.capacitors = []
		self.nodes = set()

		self.time_step = None

	def _add_resistor(self, resistance, node1, node2):
		self.resistors.append(Resistor(resistance+1e-7, node1, node2))
		self.nodes.update([node1, node2])
		self.update_node_index()

	def _add_voltage_source(self, voltage, node1, node2):
		self.voltage_sources.append(VoltageSource(voltage, node1, node2))
		self.nodes.update([node1, node2])
		self.update_node_index()

	def _add_capacitor(self, capacitance, node1, node2, initial_voltage=0):
		self.capacitors.append(Capacitor(capacitance, node1, node2, initial_voltage))
		self.nodes.update([node1, node2])
		self.update_node_index()

	def _add_diode(self, node1, node2):
		self.diodes.append(Diode(node1, node2))
		self.nodes.update([node1, node2])
		self.update_node_index()
	
	def add(self, component):
		match component.__class__.__name__:
			case "Resistor":
				self._add_resistor(component.resistance+1e-7, component.node1, component.node2)
			case "VoltageSource":
				self._add_voltage_source(component.voltage, component.node1, component.node2)
			case "Capacitor":
				self._add_capacitor(component.capacitance, component.node1, component.node2, component.initial_voltage)
			case "Diode":
				self._add_diode(component.node1, component.node2)
			case _:
				raise TypeError("unknown component")

	def update_node_index(self):
		self.node_index = {node: index for index, node in enumerate(self.nodes)}

	def _increment(self, time_step):
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

	def get_solver(self, time_step) -> "CircuitSolver":
		if time_step <= 0:
			raise ValueError("time_step should be positive")

		return CircuitSolver(self, time_step)

class CircuitSolver:
	def __init__(self, circuit: Circuit, time_step: float = 1):
		self.circuit = circuit
		self.time_step = time_step
	
	def solve(self, t_max, *, progressbar=True):
		if t_max <= 0:
			raise ValueError("t_max should be positive")
		
		if t_max < self.time_step:
			raise ValueError("t_max must be greater or equal to time_step")

		r = range(int(t_max // self.time_step))
		if progressbar:
			r = tqdm(r)
		
		incrementer = self.circuit._increment(self.time_step)

		for _ in r:
			voltages = incrementer.__next__()

		return voltages
