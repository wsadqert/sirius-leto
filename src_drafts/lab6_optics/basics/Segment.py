import math

from .Point import Point
from .GeometryBasic import GeometryBasic


__all__ = ["Segment"]

class Segment(GeometryBasic):
	def __init__(self, point_1: Point, point_2: Point):
		self.x1 = point_1.x
		self.y1 = point_1.y
		self.x2 = point_2.x
		self.y2 = point_2.y
	
	@classmethod
	def from_points(cls, point_1: Point, point_2: Point):
		return cls(point_1, point_2)
	
	@classmethod
	def from_polar(cls, point_1: Point, angle: float, length: float):
		x2 = point_1.x + length * math.cos(math.radians(angle))
		y2 = point_1.y + length * math.sin(math.radians(angle))
		return cls(point_1, Point(x2, y2))

	@property
	def angle(self):
		return math.degrees(math.atan2(self.y2 - self.y1, self.x2 - self.x1))

	@property
	def length(self):
		return math.sqrt((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2)

	def get_points(self):
		return (
			Point(self.x1, self.y1), 
			Point(self.x2, self.y2)
		)
