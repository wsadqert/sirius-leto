from typing import Sequence
from multipledispatch import dispatch
import math
from . import Point

__all__ = ["Segment"]

class Segment:
	@dispatch(Point, Point)
	def __init__(self, point_1: Point, point_2: Point):
		self.x1 = point_1.x
		self.y1 = point_1.y
		self.x2 = point_2.x
		self.y2 = point_2.y
	
	@dispatch(Sequence[Point])
	def __init__(self, points: Sequence[Point]):
		self.x1 = points[0].x
		self.y1 = points[0].y
		self.x2 = points[1].x
		self.y2 = points[1].y
	
	@classmethod
	def from_points(cls, point_1: Point, point_2: Point):
		return cls(point_1, point_2)
	
	@classmethod
	def from_polar(cls, point_1: Point, angle, length):
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
