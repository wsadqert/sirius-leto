import math
from math import pi

from . import Point

__all__ = ["Ray"]

class Ray:
	def __init__(self):
		self.x1 = 0
		self.y1 = 0
		self.x2 = 0
		self.y2 = 0
		self.angle = 0
		self.length = 0
	
	@classmethod
	def from_points(cls, point_1: Point, point_2: Point):
		self = cls.__new__(cls)

		self.x1 = point_1.x
		self.y1 = point_1.y
		self.x2 = point_2.x
		self.y2 = point_2.y

		self.angle = math.atan2(self.y2 - self.y1, self.x2 - self.x1)
		self.length = math.sqrt((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2)

		return self

	@classmethod
	def from_polar(cls, point_1: Point, length: float, angle: float):
		self = cls.__new__(cls)
		
		angle /= -180 / pi

		self.x1 = point_1.x
		self.y1 = point_1.y
		self.x2 = point_1.x + length * math.cos(angle)
		self.y2 = point_1.y + length * math.sin(angle)
		self.angle = angle
		self.length = length

		return self
	
	@classmethod
	def from_angle(cls, point_1: Point, angle: float):
		self = cls.__new__(cls)
		
		length = 1000
		angle /= -180 / pi

		self.x1 = point_1.x
		self.y1 = point_1.y
		self.x2 = point_1.x + length * math.cos(angle)
		self.y2 = point_1.y + length * math.sin(angle)
		self.angle = angle
		self.length = float("inf")

		return self

	def get_points(self):
		return (
			Point(self.x1, self.y1),
			Point(self.x2, self.y2)
		)
