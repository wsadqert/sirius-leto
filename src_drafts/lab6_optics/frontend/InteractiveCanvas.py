import tkinter as tk
from tkinter import Canvas

__all__ = ["InteractiveCanvas"]

class InteractiveCanvas(Canvas):
	def __init__(self, master, config: dict[str, any], *args, **kwargs):
		super().__init__(master, config, *args, **kwargs)

		# for key, value in (config.__dict__.copy() | kwargs).items():
		# 	try:
		# 		self.config({key: value})
		# 	except tk.TclError as e:
		# 		print(e)

		self.bind("<Button-1>", self.on_button_press)
		self.bind("<B1-Motion>", self.on_mouse_drag)
		self.bind("<MouseWheel>", self.on_mouse_wheel)

		self.start_x = None
		self.start_y = None

		self.dx_total = 0
		self.dy_total = 0

		self.objects = []

		# scaling
		self.scale_factor = 1.0
		self.bind("<MouseWheel>", self.on_mouse_wheel)

	def on_mouse_wheel(self, event):
		mouse_x = self.winfo_pointerx() - self.winfo_rootx()
		mouse_y = self.winfo_pointery() - self.winfo_rooty()

		if event.delta > 0:
			scale_change = 1.1
		else:
			scale_change = 1 / 1.1

		self.scale("all", mouse_x, mouse_y, scale_change, scale_change)

		self.scale_factor *= scale_change

		self.configure(scrollregion=self.bbox("all"))

	def on_button_press(self, event):
		self.start_x = event.x
		self.start_y = event.y

	def on_mouse_drag(self, event):
		dx = event.x - self.start_x
		dy = event.y - self.start_y

		self.dx_total += dx
		self.dy_total += dy

		for obj in self.objects:
			self.move(obj, dx, dy)

		self.start_x = event.x
		self.start_y = event.y

	def on_button_release(self, _event):
		self.start_x = None
		self.start_y = None
