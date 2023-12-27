import tkinter as tk
from typing import Callable

__all__ = ["AnimationControlButton"]


class AnimationControlButton(tk.Button):
	def __init__(self, root: tk.Tk | tk.Frame, image: tk.Image, command: Callable = lambda x: x):
		assert image

		self.photo = image

		super().__init__(
			root,
			image=image,
			command=command,
			compound=tk.LEFT
		)
