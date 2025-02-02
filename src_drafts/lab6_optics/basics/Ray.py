import math
from math import pi

from .Point import Point
from .GeometryBasic import GeometryBasic

__all__ = ["Ray"]

class Ray(GeometryBasic):
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
		angle_rad = math.radians(angle)

		self.x1 = point_1.x
		self.y1 = point_1.y
		self.x2 = point_1.x + length * math.cos(angle_rad)
		self.y2 = point_1.y + length * math.sin(angle_rad)
		self.angle = angle
		self.length = math.sqrt((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2)

		return self

	def modify(self, parameter: str, new_value):
		match parameter:
			case "angle":
				# saving point_1, length
				self.angle = new_value
				self.x2 = self.x1 + self.length * math.cos(self.angle)
				self.y2 = self.y1 + self.length * math.sin(self.angle)

			case "length":
				# saving point_1, angle
				self.length = new_value
				self.x2 = self.x1 + self.length * math.cos(self.angle)
				self.y2 = self.y1 + self.length * math.sin(self.angle)

			case "point_1":
				# saving point_2
				self.x1 = new_value.x
				self.y1 = new_value.y
				self.angle = math.atan2(self.y2 - self.y1, self.x2 - self.x1)
				self.length = math.sqrt((self.x2 - self.x1)**2 + (self.y2 - self.y1)**2)

			case "point_2":
				# saving point_1
				self.x2 = new_value.x
				self.y2 = new_value.y
				self.angle = math.atan2(self.y2 - self.y1, self.x2 - self.x1)
				self.length = math.sqrt((self.x2 - self.x1)**2 + (self.y2 - self.y1)**2)

			case "name":
				self.name = new_value

			case _:
				raise ValueError("Invalid parameter")

	def get_points(self):
		return (
			Point(self.x1, self.y1),
			Point(self.x2, self.y2)
		)

	def __add__(self, other: Point):
		return self.move(other.x, other.y)
