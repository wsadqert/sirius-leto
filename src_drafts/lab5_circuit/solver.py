import numpy as np
from tqdm import tqdm
from components.abc import *
from components import *
from exceptions import *

class ComponentsList:
	def __init__(self):
		self._components_dict = {}

	def __getitem__(self, key):
		return self._components_dict.get(key, [])
	
	def append(self, key, value):
		self._components_dict[key] = self[key] + [value]


class Circuit:
	def __init__(self):
		self.instrumental_precise = 1e-5
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
			component.set_presise(self.instrumental_precise)


		elif isinstance(component, Resistor):
			component.value += 1e-7  # Add a small value to avoid division by zero

		self.components.append(component.__class__.__name__, component)
		self.nodes.update([component.node1, component.node2])
		self.update_node_index()
	
	def update_node_index(self):
		self.node_index = {node: index for index, node in enumerate(self.nodes)}

	def set_instrumental_precise(self, precise: float):
		if precise < 0:
			raise InstrumentError("Precision must be non-negative")
		
		self.instrumental_precise = precise
		
		for instr in self.components['Instrument']:
			instr.set_presise(precise)

	def _increment(self, time_step):
		time = 0
		voltages = {node: 0 for node in self.nodes}  # Initial voltages at nodes
		voltages['ground'] = 0

		while True:
			# Build equations based on KCL for each node (except ground)
			A = np.zeros((len(self.nodes), len(self.nodes)))
			B = np.zeros(len(self.nodes))

			for node in self.nodes:
				if node == 'ground':
					continue

				node_eq_index = self.node_index[node]

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
						B[node_eq_index] -= source.value
						A[node_eq_index, node_eq_index] += 1  # KVL for voltage source
						A[node_eq_index, other_node_index] -= 1  # KVL for voltage source
					elif source.node2 == node:
						other_node_index = self.node_index[source.node1]
						B[node_eq_index] += source.value
						A[node_eq_index, node_eq_index] += 1  # KVL for voltage source
						A[node_eq_index, other_node_index] -= 1  # KVL for voltage source

				for diode in self.components["Diode"]:
					if diode.node1 == node:  # Diode is forward biased, current can flow
						other_node_index = self.node_index[diode.node2]
						A[node_eq_index, node_eq_index] += 1
						A[node_eq_index, other_node_index] -= 1
					elif diode.node2 == node:  # Diode is reverse biased
						other_node_index = self.node_index[diode.node1]
						# No changes to A or B since current cannot flow

				for capacitor in self.components["Capacitor"]:
					if capacitor.node1 == node:
						other_node_index = self.node_index[capacitor.node2]
						dV_dt = (voltages[capacitor.node1] - voltages[capacitor.node2]) / time_step
						current = capacitor.value * dV_dt
						A[node_eq_index, node_eq_index] += 1
						A[node_eq_index, other_node_index] -= 1
						B[node_eq_index] += current
					elif capacitor.node2 == node:
						other_node_index = self.node_index[capacitor.node1]
						dV_dt = (voltages[capacitor.node2] - voltages[capacitor.node1]) / time_step
						current = capacitor.value * dV_dt
						A[node_eq_index, node_eq_index] += 1
						A[node_eq_index, other_node_index] -= 1
						B[node_eq_index] += current
				
				for ammeter in self.components["Ammeter"]:
					if ammeter.node1 == node:
						if ammeter.node2 in self.node_index:
							other_node_index = self.node_index[ammeter.node2]
							A[node_eq_index, node_eq_index] += 1 / ammeter.resistance
							A[node_eq_index, other_node_index] -= 1 / ammeter.resistance
					elif ammeter.node2 == node:
						if ammeter.node1 in self.node_index:
							other_node_index = self.node_index[ammeter.node1]
							A[node_eq_index, node_eq_index] += 1 / ammeter.resistance
							A[node_eq_index, other_node_index] -= 1 / ammeter.resistance

			# Set ground node voltage to 0
			ground_index = self.node_index['ground']
			A[ground_index, :] = 0
			A[ground_index, ground_index] = 1
			B[ground_index] = 0

			# Enforce the voltage of the voltage sources
			for source in self.components["VoltageSource"]:
				if source.node1 == 'ground':
					node_eq_index = self.node_index[source.node2]
					B[node_eq_index] = source.value  # Set the voltage to the source voltage
					A[node_eq_index, :] = 0  # Clear the equation for this node
					A[node_eq_index, node_eq_index] = 1  # Set the voltage at this node
				elif source.node2 == 'ground':
					node_eq_index = self.node_index[source.node1]
					B[node_eq_index] = -source.value  # Set the voltage to the source voltage (negative)
					A[node_eq_index, :] = 0  # Clear the equation for this node
					A[node_eq_index, node_eq_index] = 1  # Set the voltage at this node


			# Solve the linear equations for the current time step
			try:
				voltages = dict(zip(self.nodes, np.linalg.solve(A, B).copy()))
			except:
				raise CannotSolve("Circuit cannot be solved successfully")

			self.is_calculated = True
			self.voltages = voltages

			yield voltages

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