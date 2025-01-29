import math
from dataclasses import dataclass

__all__ = ["Vector"]

@dataclass
class Vector:
	x: float = 0
	y: float = 0

	def to_tuple(self) -> tuple[float, float]:
		return self.x, self.y

	def rotate(self, angle: float) -> "Vector":
		angle = math.degrees(angle)
		
		return Vector(
			self.x * math.cos(angle) - self.y * math.sin(angle), 
			self.x * math.sin(angle) + self.y * math.cos(angle)
		)

	def __add__(self, other: "Vector") -> "Vector":
		return Vector(self.x + other.x, self.y + other.y)

	def __sub__(self, other: "Vector") -> "Vector":
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
