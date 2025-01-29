import math
from .abc import Active
from basics import Ray, Point, Segment

__all__ = ["Lens"]

class Lens(Active):
	def __init__(self, name: str, center: Point, radius: float, angle: float, focus: float, *args, **kwargs):
		# size_x = 0
		# size_y = 2 * radius - don't use!
		super().__init__(name, center, 0, 2*radius, angle, *args, **kwargs)

		self.radius = radius
		self.focus = focus
	
	def get_points(self) -> tuple[Point, Point]:
		x1 = self.x - self.radius * math.cos(self.angle)
		y1 = self.y - self.radius * math.sin(self.angle)
		x2 = self.x + self.radius * math.cos(self.angle)
		y2 = self.y + self.radius * math.sin(self.angle)

		return (
			Point(x1, y1),
			Point(x2, y2)
		)


	def apply(self, ray: Ray) -> Ray:
		lens_segment = Segment(self.get_points())
		
		pass
		return ray
