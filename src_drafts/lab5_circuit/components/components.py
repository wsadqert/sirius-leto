from .abc import Component

__all__ = ["VoltageSource", "Resistor", "Wire", "Diode", "Capacitor"]

class VoltageSource(Component):
	def __init__(self, voltage, node1, node2):
		super().__init__(voltage, node1, node2)

class Resistor(Component):
	def __init__(self, resistance, node1, node2):
		super().__init__(resistance, node1, node2)

class Wire(Resistor):
	def __init__(self, node1, node2):
		super().__init__(0, node1, node2)

class Diode(Component):
	def __init__(self, node1, node2):
		super().__init__(None, node1, node2)

class Capacitor(Component):
	def __init__(self, capacitance, node1, node2, initial_charge=0):
		super().__init__(capacitance, node1, node2)

		self.voltage = 0
		self.previous_voltage = 0
		self.charge = initial_charge

class Inductor(Component):
	def __init__(self, inductance, node1, node2):
		super().__init__(inductance, node1, node2)

		self.current = 0
