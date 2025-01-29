from abc import abstractmethod
from components.abc import Component

from basics import Point, Ray

class Source(Component):
	def __init__(self, name: str, point: Point, *args, intensity: float = 1, **kwargs):
		super().__init__(name, point, *args, **kwargs)

		self.intensity: float = intensity

	@abstractmethod
	def get_rays(self) -> list[Ray]:
		pass
