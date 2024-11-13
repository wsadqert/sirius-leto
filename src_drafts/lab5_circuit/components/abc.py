import abc
from exceptions import InstrumentError

__all__ = ["Component", "Instrument"]

class Component(abc.ABC):
	def __init__(self, value, node1, node2):
		self.value = value
		self.node1 = node1
		self.node2 = node2

class Instrument(Component):
	def __init__(self, node1, node2):
		super().__init__(None, node1, node2)

		self.circuit: "Circuit" = None
	
	def set_circuit(self, circuit: "Circuit"):
		self.circuit = circuit

	def _check_connectivity(self):
		if self.circuit is None:
			return InstrumentError("instrument is not connected to circuit")
		
		if not self.circuit.is_calculated:
			return InstrumentError("instrument cannot be used until the circuit has been calculated for at least 1 iteration")
	
	@abc.abstractmethod
	def get_value(self):
		pass
