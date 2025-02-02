from abc import abstractmethod

from components.abc import Component
from basics import Ray, Point

class Active(Component):
	def __init__(self, name: str, point: Point, size_x: float, size_y: float, angle: float, *args, **kwargs):
		super().__init__(name, point, *args, **kwargs)
		
		self.size_x = size_x
		self.size_y = size_y
		self.angle = angle

	@abstractmethod
	def apply(self, ray: Ray) -> Ray:
		pass
	
	@abstractmethod
	def get_points(self) -> list[Point]:
		pass

	@abstractmethod
	def is_intersects(self, ray: Ray) -> bool:
		pass
