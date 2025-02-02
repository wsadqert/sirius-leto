from dataclasses import dataclass

from .GeometryBasic import GeometryBasic

__all__ = ["Point"]

@dataclass
class Point(GeometryBasic):
	x: float = 0
	y: float = 0

	def __post_init__(self):
		del self.x1, self.y1, self.x2, self.y2

	def to_tuple(self) -> tuple[float, float]:
		return self.x, self.y

	def __add__(self, other: "Point") -> "Point":
		return Point(self.x + other.x, self.y + other.y)
	
	def __sub__(self, other: "Point") -> "Point":
		return Point(self.x - other.x, self.y - other.y)

	def __eq__(self, other: "Point") -> bool:
		return self.x == other.x and self.y == other.y
