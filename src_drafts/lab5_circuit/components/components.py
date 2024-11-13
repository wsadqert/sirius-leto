from .abc import Component

__all__ = ["VoltageSource", "Resistor", "Diode", "Capacitor"]

class VoltageSource(Component):
	def __init__(self, voltage, node1, node2):
		super().__init__(voltage, node1, node2)

class Resistor(Component):
	def __init__(self, resistance, node1, node2):
		super().__init__(resistance, node1, node2)

class Diode(Component):
	def __init__(self, node1, node2):
		super().__init__(None, node1, node2)

class Capacitor(Component):
	def __init__(self, capacitance, node1, node2, initial_voltage=0):
		super().__init__(capacitance, node1, node2)

		self.initial_voltage = initial_voltage
		self.current = 0
