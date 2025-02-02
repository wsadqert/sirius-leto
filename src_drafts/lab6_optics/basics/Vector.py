import math
from dataclasses import dataclass
from typing import Union

from basics import Point

from .GeometryBasic import GeometryBasic

__all__ = ["Vector"]


@dataclass
class Vector(GeometryBasic):
	x: float = 0
	y: float = 0

	def to_tuple(self) -> tuple[float, float]:
		return self.x, self.y

	def rotate(self, angle: float) -> "Vector":
		"""
		Rotates the vector counterclockwise by the given angle in degrees.
		"""

		angle = math.radians(angle)

		return Vector(
			self.x * math.cos(angle) - self.y * math.sin(angle),
			self.x * math.sin(angle) + self.y * math.cos(angle),
		)
	
	@classmethod
	def from_points(cls, point_1: Point, point_2: Point):
		return cls(point_2.x - point_1.x, point_2.y - point_1.y)
	
	@classmethod
	def from_point(cls, point: Point):
		return cls(point.x, point.y)
	
	@classmethod
	def from_polar(cls, length: float, angle: float):
		return cls(
			length * math.cos(math.radians(angle)), 
			length * math.sin(math.radians(angle))
		)

	def __add__(self, other: Union["Vector", Point]) -> "Vector":
		return Vector(self.x + other.x, self.y + other.y)

	def __sub__(self, other: Union["Vector", Point]) -> "Vector":
		return Vector(self.x - other.x, self.y - other.y)

	def __mul__(self, scalar: float) -> "Vector":
		return Vector(self.x * scalar, self.y * scalar)

	def __eq__(self, other: "Vector") -> bool:
		if isinstance(other, int):
			if other == 0:
				return self.x == 0 and self.y == 0
			else:
				return False

		elif isinstance(other, Vector):
			return self.x == other.x and self.y == other.y

		return False

	def __bool__(self):
		return self.x != 0 or self.y != 0
