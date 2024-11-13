from .abc import Instrument

__all__ = ["Voltmeter"]

class Voltmeter(Instrument):
	def __init__(self, node1, node2):
		super().__init__(node1, node2)
	
	def get_value(self):
		self._check_connectivity()

		return self.circuit.voltages[self.node1] - self.circuit.voltages[self.node2]
	
	def set_circuit(self, circuit: "Circuit"):
		self.circuit = circuit
		return super().set_circuit(circuit)

class Ammeter(Instrument):
	def __init__(self, node1, node2):
		super().__init__(node1, node2)
	
	def get_value(self):
		self._check_connectivity()

		raise NotImplementedError

		return self.circuit.voltages[self.node1] - self.circuit.voltages[self.node2]
	
	def set_circuit(self, circuit: "Circuit"):
		self.circuit = circuit
		return super().set_circuit(circuit)
