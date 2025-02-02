from basics import Point

__all__ = ["Component"]

class Component:
	def __init__(self, name: str, point: Point, *args, **kwargs):
		self.name = name
		self.x = point.x
		self.y = point.y
		self.args = args

		for key, value in kwargs.items():
			setattr(self, key, value)
