__all__ = ["VoltageSource", "Resistor", "Diode", "Capacitor"]

class VoltageSource:
	def __init__(self, voltage, node1, node2):
		self.voltage = voltage
		self.node1 = node1
		self.node2 = node2

class Resistor:
	def __init__(self, resistance, node1, node2):
		self.resistance = resistance
		self.node1 = node1
		self.node2 = node2

class Diode:
	def __init__(self, node1, node2):
		self.node1 = node1  # Anode
		self.node2 = node2  # Cathode

class Capacitor:
    def __init__(self, capacitance, node1, node2, initial_voltage=0):
        self.capacitance = capacitance
        self.node1 = node1
        self.node2 = node2
        self.initial_voltage = initial_voltage  # Initial voltage across the capacitor
        self.current = 0  # Current through the capacitor
