from dataclasses import dataclass
from datetime import time
from typing import Iterable
from multimethod import multimethod
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

# TODO: implement circuit config class
"""
@dataclass
class CircuitConfig:
	instrumental_precise: float
	resistance_error: float
	time_step: float
	pass
"""


class Circuit:
	def __init__(self):
		self.instrumental_precise = 1e-5
		self.resistance_error = 1e-7
		self.components = ComponentsList()

		self.nodes = set()

		self.is_calculated = False
		self.voltages = {}
	

	@multimethod
	def add(self, *args, **kwargs):
		raise ValueError("unknown parameter(s)")

	@add.register
	def _(self, component: Component):
		if not isinstance(component, Component):
			raise TypeError("unknown component")

		if isinstance(component, Instrument):
			component.set_circuit(self)
			component.set_presise(self.instrumental_precise)

		elif isinstance(component, Resistor):
			component.value += self.resistance_error  # Add a small value to avoid division by zero

		component.resistance += self.resistance_error  # Add a small value to avoid division by zero

		if isinstance(component, Wire):
			self.components.append("Resistor", component)
		else:
			self.components.append(component.__class__.__name__, component)
		
		self.nodes.update([component.node1, component.node2])
		self.update_node_index()
	
	@add.register
	def _(self, components_list: Iterable[Component]):
		for component in components_list:
			self.add(component)
	
	def update_node_index(self):
		self.node_index = {node: index for index, node in enumerate(self.nodes)}

	def set_instrumental_precise(self, precise: float):
		if precise < 0:
			raise InstrumentError("Precision must be non-negative")
		
		self.instrumental_precise = precise
		
		for instr in self.components['Instrument']:
			instr.set_presise(precise)

	def _increment(self, time_step):
		step_number = 0
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
					elif resistor.node2 == node:
						other_node_index = self.node_index[resistor.node1]
					else: continue

					A[node_eq_index, node_eq_index] += 1 / resistor.value
					A[node_eq_index, other_node_index] -= 1 / resistor.value

				for source in self.components["VoltageSource"]:
					if source.node1 == node:
						other_node_index = self.node_index[source.node2]
						B[node_eq_index] -= source.value
					elif source.node2 == node:
						other_node_index = self.node_index[source.node1]
						B[node_eq_index] += source.value
					else: continue

					A[node_eq_index, node_eq_index] += 1 / source.resistance
					A[node_eq_index, other_node_index] -= 1 / source.resistance

				for diode in self.components["Diode"]:
					if diode.node1 == node:  # Diode is forward biased, current can flow
						other_node_index = self.node_index[diode.node2]
						A[node_eq_index, node_eq_index] += 1 / diode.resistance
						A[node_eq_index, other_node_index] -= 1 / diode.resistance
					elif diode.node2 == node:  # Diode is reverse biased
						# No changes to A or B since current cannot flow
						pass
				
				for capacitor in self.components["Capacitor"]:
					if capacitor.node1 == node:
						other_node_index = self.node_index[capacitor.node2]
					elif capacitor.node2 == node:
						other_node_index = self.node_index[capacitor.node1]
					else: continue

					if step_number == 0:
						# Assume zero-resistance at the beginning of the simulation
						A[node_eq_index, node_eq_index] += 1 / capacitor.resistance
						A[node_eq_index, other_node_index] -= 1 / capacitor.resistance
						continue

					elif step_number == 1:
						# 
						capacitor.voltage = voltages[capacitor.node1] - voltages[capacitor.node2]
						current = capacitor.voltage / capacitor.resistance
						print(current)
					
					else:
						current = capacitor.value * (capacitor.voltage - capacitor.previous_voltage) / time_step
						print(f"{current = }")
					
					capacitor.charge += current * time_step
					capacitor.previous_voltage = capacitor.voltage

					if step_number != 1:
						capacitor.voltage = capacitor.charge / capacitor.value

					# Enforce the capacitor's voltage in the system of equations
					if capacitor.node1 == node:
						A[node_eq_index, node_eq_index] += 1
						A[node_eq_index, other_node_index] -= 1
						B[node_eq_index] -= capacitor.voltage
					elif capacitor.node2 == node:
						A[node_eq_index, node_eq_index] += 1
						A[node_eq_index, other_node_index] -= 1
						B[node_eq_index] += capacitor.voltage

					print(f"{capacitor.voltage = }")

				"""
				for inductor in self.components["Inductor"]:
					if inductor.node1 == node:
						other_node_index = self.node_index[inductor.node2]
						voltage_across = voltages[inductor.node1] - voltages[inductor.node2]
					elif inductor.node2 == node:
						other_node_index = self.node_index[inductor.node1]
						voltage_across = voltages[inductor.node2] - voltages[inductor.node1]
					else: continue
					current_change = voltage_across / inductor.value
					inductor.current += current_change * time_step
					A[node_eq_index, node_eq_index] += 1
					A[node_eq_index, other_node_index] -= 1
					B[node_eq_index] += voltage_across
				"""
				
				for ammeter in self.components["Ammeter"]:
					if ammeter.node1 == node:
						other_node_index = self.node_index[ammeter.node2]
					elif ammeter.node2 == node:
						other_node_index = self.node_index[ammeter.node1]
					else: continue
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
			step_number += 1

			yield voltages


	def get_solver(self, time_step) -> "CircuitSolver":
		if time_step <= 0:
			raise ValueError("time_step should be positive")

		return CircuitSolver(self, time_step)

class CircuitSolver:
	def __init__(self, circuit: Circuit, time_step: float):
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
