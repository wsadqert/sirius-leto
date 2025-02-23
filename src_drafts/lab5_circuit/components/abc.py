import abc
from exceptions import InstrumentError

__all__ = ["Component", "Instrument"]

class Component(abc.ABC):
	def __init__(self, value, node1, node2):
		self.value = value
		self.node1 = node1
		self.node2 = node2
		self.resistance = 0
	
	def __repr__(self):
		return f"{self.__class__.__name__}({self.value}) between ({self.node1}, {self.node2})"

	def __str__(self):
		return f"{self.__class__.__name__}({self.value}) between ({self.node1}, {self.node2})"

class Instrument(Component):
	def __init__(self, node1, node2):
		self._precise = 0
		super().__init__(None, node1, node2)

		self.circuit: "Circuit" = None

	def set_presise(self, precise):
		if precise < 0:
			raise InstrumentError("Precision must be non-negative")
		self._precise = precise

	def set_circuit(self, circuit: "Circuit"):
		self.circuit = circuit

	def _check_connectivity(self):
		if self.circuit is None:
			raise InstrumentError("instrument is not connected to circuit")
		
		if not self.circuit.is_calculated:
			raise InstrumentError("instrument cannot be used until the circuit has been calculated for at least 1 iteration")
	
	@abc.abstractmethod
	def get_value(self):
		pass

	def __repr__(self):
		return f"{self.__class__.__name__} at {self.circuit} between ({self.node1}, {self.node2})"

	def __str__(self):
		return f"{self.__class__.__name__} at {self.circuit} between ({self.node1}, {self.node2})"
