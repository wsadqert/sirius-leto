import math
import tkinter as tk
from basics import *
from components.actives import Lens
from components.sources import *

class RayTracingApp:
	def __init__(self, master):
		self.master = master
		self.canvas = tk.Canvas(
			master, 
			width=800, 
			height=600, 
			bg='black'
		)
		self.canvas.pack()

		self.lasers = [
			laser_1 := Laser("Laser1", Point(400, 300), angle=-30)
		]
		self.lamps = [
			Lamp("Lamp1", Point(300, 300))
		]

		lens_1 = Lens(
			name="Lens1",
			center = Point(500, 400),
			radius=100,
			angle=0,
			focus=500
		)


		self.lenses = [lens_1]

		self.sources = self.lamps + self.lasers

		# dragging
		self.canvas.bind("<ButtonPress-1>", self.on_button_press)
		self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
		self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

		self.start_x = None
		self.start_y = None

		self.dx_total = 0
		self.dy_total = 0
		
		self.objects = []

		# scaling
		self.scale_factor = 1.0
		self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)

		# drawing
		self.draw_lens(lens_1)
		self.draw_ray(lens_1.apply(laser_1.get_rays()[0]))
		self.draw_rays()

	def on_mouse_wheel(self, event):
		# зиг хайль
		mouse_x = self.canvas.winfo_pointerx() - self.canvas.winfo_rootx()
		mouse_y = self.canvas.winfo_pointery() - self.canvas.winfo_rooty()

		if event.delta > 0:
			scale_change = 1.1
		else:
			scale_change = 1 / 1.1

		self.canvas.scale("all", mouse_x, mouse_y, scale_change, scale_change)

		self.scale_factor *= scale_change

		self.canvas.configure(scrollregion=self.canvas.bbox("all"))

	def draw_ray(self, ray: Ray):
		x1, y1, x2, y2 = ray.get_points()
		line = self.canvas.create_line(
			x1 + self.dx_total, 
			y1 + self.dy_total, 
			x2 + self.dx_total, 
			y2 + self.dy_total, 
			fill='#ffff90',
			width=1
		)

		self.objects.append(line)
		pass

	def draw_rays(self):
		for source in self.sources:
			rays = source.get_rays()
			for ray in rays:
				self.draw_ray(ray)
			
			source_icon = self.canvas.create_oval(
				source.x - 5 + self.dx_total, 
				source.y - 5 + self.dy_total, 
				source.x + 5 + self.dx_total, 
				source.y + 5 + self.dy_total, 
				fill='white', 
				outline='black'
			)
			self.objects.append(source_icon)
		
	def draw_lens(self, lens: Lens):
		x = lens.x
		y = lens.y
		size = lens.size_y
		angle = lens.angle

		line = self.canvas.create_line(
			x - size/2 * math.sin(angle) + self.dx_total, 
			y - size/2 * math.cos(angle) + self.dy_total, 
			x + size/2 * math.sin(angle) + self.dx_total, 
			y + size/2 * math.cos(angle) + self.dy_total, 
			fill='#ffff90',
			width=10
		)

		self.objects.append(line)

	def on_button_press(self, event):
		self.start_x = event.x
		self.start_y = event.y

	def on_mouse_drag(self, event):
		dx = event.x - self.start_x
		dy = event.y - self.start_y

		self.dx_total += dx
		self.dy_total += dy

		for obj in self.objects:
			self.canvas.move(obj, dx, dy)

		self.start_x = event.x
		self.start_y = event.y

	def on_button_release(self, _event):
		self.start_x = None
		self.start_y = None
		
if __name__ == "__main__":
	root = tk.Tk()
	app = RayTracingApp(root)
	root.mainloop()
