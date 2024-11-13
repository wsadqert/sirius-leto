from annotated_types import IsInfinite
import numpy as np
from tqdm import tqdm
from components.abc import *
from components import *

class ComponentsList:
	def __init__(self):
		self._components_dict = {}
		pass

	def __getitem__(self, key):
		return self._components_dict.get(key, [])
	
	def append(self, key, value):
		self._components_dict[key] = self[key] + [value]


class Circuit:
	def __init__(self):
		self.components = ComponentsList()

		self.nodes = set()

		self.is_calculated = False
		self.voltages = {}

		self.time_step = None

	def add(self, component: Component):
		if not isinstance(component, Component):
			raise TypeError("unknown component")

		if isinstance(component, Instrument):
			component.circuit = self

		self.components.append(component.__class__.__name__, component)
		self.nodes.update([component.node1, component.node2])
		self.update_node_index()
	
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

				for resistor in self.components["Resistor"]:
					if resistor.node1 == node:
						other_node_index = self.node_index[resistor.node2]
						A[node_eq_index, node_eq_index] += 1 / resistor.value
						A[node_eq_index, other_node_index] -= 1 / resistor.value
					elif resistor.node2 == node:
						other_node_index = self.node_index[resistor.node1]
						A[node_eq_index, node_eq_index] += 1 / resistor.value
						A[node_eq_index, other_node_index] -= 1 / resistor.value

				for source in self.components["VoltageSource"]:
					if source.node1 == node:
						other_node_index = self.node_index[source.node2]
						A[node_eq_index, node_eq_index] += 1  # KVL for voltage source
						A[node_eq_index, other_node_index] -= 1  # KVL for voltage source
						B[node_eq_index] -= source.value
					elif source.node2 == node:
						other_node_index = self.node_index[source.node1]
						A[node_eq_index, node_eq_index] += 1  # KVL for voltage source
						A[node_eq_index, other_node_index] -= 1  # KVL for voltage source
						B[node_eq_index] += source.value

				for diode in self.components["Diode"]:
					if diode.node1 == node:  # Diode is forward biased
						other_node_index = self.node_index[diode.node2]
						A[node_eq_index, node_eq_index] += 1  # Current can flow
						A[node_eq_index, other_node_index] -= 1  # Current can flow
					elif diode.node2 == node:  # Diode is reverse biased
						other_node_index = self.node_index[diode.node1]
						# No changes to A or B since current cannot flow

				# Add equations for capacitors
				for capacitor in self.components["Capacitor"]:
					if capacitor.node1 == node:
						other_node_index = self.node_index[capacitor.node2]
						dV_dt = (voltages[capacitor.node1] - voltages[capacitor.node2]) / time_step
						current = capacitor.value * dV_dt
						A[node_eq_index, node_eq_index] += 1  # Current can flow
						A[node_eq_index, other_node_index] -= 1  # Current can flow
						B[node_eq_index] += current  # Add the current to the B matrix
					elif capacitor.node2 == node:
						other_node_index = self.node_index[capacitor.node1]
						dV_dt = (voltages[capacitor.node2] - voltages[capacitor.node1]) / time_step
						current = capacitor.value * dV_dt
						A[node_eq_index, node_eq_index] += 1  # Current can flow
						A[node_eq_index, other_node_index] -= 1  # Current can flow
						B[node_eq_index] += current  # Add the current to the B matrix

			# Set ground node voltage to 0
			ground_index = self.node_index['ground']
			A[ground_index, :] = 0
			A[ground_index, ground_index] = 1
			B[ground_index] = 0

			# Enforce the voltage of the voltage sources
			for source in self.components["VoltageSource"]:
				if source.node1 == 'ground':
					node_eq_index = self.node_index[source.node2]
					A[node_eq_index, :] = 0  # Clear the equation for this node
					A[node_eq_index, node_eq_index] = 1  # Set the voltage at this node
					B[node_eq_index] = source.value  # Set the voltage to the source voltage
				elif source.node2 == 'ground':
					node_eq_index = self.node_index[source.node1]
					A[node_eq_index, :] = 0  # Clear the equation for this node
					A[node_eq_index, node_eq_index] = 1  # Set the voltage at this node
					B[node_eq_index] = -source.value  # Set the voltage to the source voltage (negative)


			# Solve the linear equations for the current time step
			voltages = dict(zip(self.nodes, np.linalg.solve(A, B).copy()))

			self.is_calculated = True
			self.voltages = voltages

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
