import math
from .abc import Source
from basics import Ray, Point

__all__ = ["Lamp"]

class Lamp(Source):
	def __init__(self, name: str, point: Point, intensity: float = 1):
		super().__init__(name, point, intensity = intensity)

		self.NUM_RAYS = 36
		self.ray_angles = [360 * i / self.NUM_RAYS for i in range(self.NUM_RAYS)]

	def get_rays(self) -> list[Ray]:
		return [Ray.from_angle(Point(self.x, self.y), angle) for angle in self.ray_angles]
