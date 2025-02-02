import math
from .abc import Active
from basics import *
from geometry import ray_segment_intersection

__all__ = ["Mirror"]

class Mirror(Active):
	def __init__(self, name: str, center: Point, size: float, angle: float, *args, **kwargs):
		super().__init__(name, center, size, size, angle, *args, **kwargs)

		self.size = size

	def get_points(self) -> tuple[Point, Point]:
		angle_rad = math.radians(self.angle)

		x1 = self.x - self.size / 2 * math.cos(angle_rad)
		y1 = self.y - self.size / 2 * math.sin(angle_rad)
		x2 = self.x + self.size / 2 * math.cos(angle_rad)
		y2 = self.y + self.size / 2 * math.sin(angle_rad)
		
		return (
			Point(x1, y1),
			Point(x2, y2)
		)
	
	def is_intersects(self, ray: Ray) -> bool:
		return ray_segment_intersection(Segment.from_points(*self.get_points()), ray) is not None

	def apply(self, ray: Ray):
		lens_segment = Segment.from_points(*self.get_points())

		intersect_point = ray_segment_intersection(lens_segment, ray)

		print(intersect_point)

		if intersect_point is None:
			return ray
		
		new_angle = 2 * self.angle - ray.angle
		new_ray = Ray.from_angle(intersect_point, new_angle)

		return new_ray
