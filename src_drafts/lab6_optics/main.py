from rich.traceback import install
install(show_locals=True, width=300)

from tkinter import Tk
import numpy as np

from parser import parse_config
from frontend import Drawer, InteractiveCanvas
from frontend import DrawerConfig, TraceConfig
from basics import *
from components import *


class RayTracingApp:
	def __init__(self, master):
		self.master = master

		frontend_config_raw = parse_config(".config/frontend.cfg")
		trace_config_raw = parse_config(".config/trace.cfg")
		drawer_config = DrawerConfig(**frontend_config_raw['Drawer'])
		self.trace_config = TraceConfig(**trace_config_raw['raytrace'])

		self.canvas = InteractiveCanvas(master, dict(frontend_config_raw['tcl']))
		self.canvas.pack()

		self.drawer = Drawer(self.canvas, drawer_config)

		self.create_components()
		self.draw_rays()

	def create_components(self):
		self.lasers = [
			Laser("Laser1", Point(400, 300), angle=30)
		]
		self.lamps = [
			# Lamp("Lamp1", Point(300, 300))
		]
		self.lenses = [
			Lens(name="Lens1", center=Point(500, 400), radius=100, angle=0, focus=500)
		]
		self.mirrors = [
			Mirror(name="Mirror1", center=Point(600, 400), size=100, angle=0)
		]

		self.sources: list[Source] = self.lamps + self.lasers
		self.actives: list[Active] = self.lenses + self.mirrors

	
	def trace(self):
		for source in self.sources:
			for ray in source.get_rays():
				pass
			
				# point_0 = Point(ray.x1, ray.y1)
				# for delta in np.array(0, ray.length, self.trace_config.step): 
				# 	pass

	def draw_rays(self):
		for source in self.sources:
			self.drawer.draw_source(source)


if __name__ == "__main__":
	root = Tk()
	app = RayTracingApp(root)
	root.mainloop()
