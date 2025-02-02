class GeometryBasic:
	x1: float = 0
	y1: float = 0
	x2: float = 0
	y2: float = 0

	def move(self, dx: float, dy: float):
		self.x1 += dx
		self.y1 += dy
		self.x2 += dx
		self.y2 += dy
