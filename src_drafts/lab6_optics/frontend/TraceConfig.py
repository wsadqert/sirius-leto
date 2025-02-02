from dataclasses import dataclass

__all__ = ["TraceConfig"]

@dataclass
class TraceConfig:
	step: float

	def __post_init__(self):
		self.step = float(self.step)
