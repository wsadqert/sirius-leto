from basics import *
from components.actives.abc import Active


class Wall(Active):
	def __init__(self, name: str, points: tuple[Point, Point], *args, **kwargs):
		super().__init__(name, Point(), 0, 0, 0, *args, **kwargs)

		self.points = points

	def get_points(self):
		return self.points

	def apply(self, ray: Ray):
		return Ray()
