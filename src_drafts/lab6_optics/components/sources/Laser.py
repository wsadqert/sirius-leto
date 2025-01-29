from .abc import Source
from basics import Ray, Point

__all__ = ["Laser"]

class Laser(Source):
	def __init__(self, name, point: Point, angle, intensity = 1):
		super().__init__(name, point, intensity = intensity, angle = angle)

	def get_rays(self) -> list[Ray]:
		return [Ray.from_angle(Point(self.x, self.y), self.angle), ]
