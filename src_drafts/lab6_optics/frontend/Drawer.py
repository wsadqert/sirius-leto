import math
import tkinter as tk

from basics import *
from components import *
from .DrawerConfig import DrawerConfig

__all__ = ["Drawer"]

class Drawer:
	def __init__(self, canvas: tk.Canvas, config: DrawerConfig = None):
		self.canvas = canvas
		self.config = config or {}

		attrs = {
			'objects': [],
			'dx_total': 0,
			'dy_total': 0,
		}
		for key, value in attrs.items():
			if getattr(self.canvas, key, None) is None:
				setattr(self.canvas, key, value)
		
	def get_canvas(self):
		return self.canvas
	
	def draw_ray(self, ray: Ray):
		point_1, point_2 = ray.get_points()
		x1 = point_1.x
		y1 = point_1.y
		x2 = point_2.x
		y2 = point_2.y

		line = self.canvas.create_line(
			x1 + self.canvas.dx_total,
			y1 + self.canvas.dy_total,
			x2 + self.canvas.dx_total,
			y2 + self.canvas.dy_total,
			fill=self.config.ray_color,
			width=self.config.ray_width,
		)

		self.canvas.objects.append(line)

	def draw_source(self, source: Source):
		rays = source.get_rays()
		for ray in rays:
			self.draw_ray(ray)

		source_icon = self.canvas.create_oval(
			source.x - self.config.source_size / 2 + self.canvas.dx_total,
			source.y - self.config.source_size / 2 + self.canvas.dy_total,
			source.x + self.config.source_size / 2 + self.canvas.dx_total,
			source.y + self.config.source_size / 2 + self.canvas.dy_total,
			fill=self.config.source_color,
			outline=self.config.source_outline_color,
		)
		self.canvas.objects.append(source_icon)

	def draw_lens(self, lens: Lens):
		x = lens.x
		y = lens.y
		size = lens.size_y
		angle = lens.angle

		line = self.canvas.create_line(
			x - size / 2 * math.sin(angle) + self.canvas.dx_total,
			y - size / 2 * math.cos(angle) + self.canvas.dy_total,
			x + size / 2 * math.sin(angle) + self.canvas.dx_total,
			y + size / 2 * math.cos(angle) + self.canvas.dy_total,
			fill=self.config.lens_color,
			width=self.config.lens_width,
		)

		self.canvas.objects.append(line)

	def draw_mirror(self, mirror: Mirror):
		x = mirror.x
		y = mirror.y
		size = mirror.size
		angle = math.radians(90-mirror.angle)
		# angle = math.radians(0)

		line = self.canvas.create_line(
			x - size / 2 * math.sin(angle) + self.canvas.dx_total,
			y - size / 2 * math.cos(angle) + self.canvas.dy_total,
			x + size / 2 * math.sin(angle) + self.canvas.dx_total,
			y + size / 2 * math.cos(angle) + self.canvas.dy_total,
			fill=self.config.mirror_color,
			width=self.config.mirror_width,
		)

		self.canvas.objects.append(line)
