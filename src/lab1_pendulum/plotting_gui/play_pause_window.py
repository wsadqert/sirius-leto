import os
from typing import Callable

import matplotlib.animation
import tkinter as tk

from src.general.constants import PROJECT_ROOT
from ._animation_control_button import AnimationControlButton

__all__ = ['PlayPauseWindow']


class PlayPauseWindow:
	def __init__(self, root: tk.Tk, animation: matplotlib.animation.FuncAnimation, back_function: Callable, forward_function: Callable):
		self.animation = animation

		root.resizable(False, False)

		self.play_image = tk.PhotoImage(file=os.path.join(PROJECT_ROOT, r"assets/play/play2_275px.png")).subsample(3, 3)
		self.pause_image = tk.PhotoImage(file=os.path.join(PROJECT_ROOT, r"assets/pause/pause2_275px.png")).subsample(3, 3)
		self.back_image = tk.PhotoImage(file=os.path.join(PROJECT_ROOT, r"assets/back1/back1_275px.png")).subsample(3, 3)
		self.forward_image = tk.PhotoImage(file=os.path.join(PROJECT_ROOT, r"assets/forward1/forward1_275px.png")).subsample(3, 3)

		self.frame = tk.Frame(root)
		self.frame.pack(side=tk.TOP)

		self.button_back = AnimationControlButton(self.frame, image=self.back_image, command=back_function)
		self.button_back.pack(side=tk.LEFT)

		self.button_playpause = AnimationControlButton(self.frame, image=self.play_image, command=self.onclick)
		self.button_playpause.pack(side=tk.LEFT)

		self.button_forward = AnimationControlButton(self.frame, image=self.forward_image, command=forward_function)
		self.button_forward.pack(side=tk.LEFT)

		root.bind("<space>", self.onclick)
		root.bind("<Left>", back_function)
		root.bind("<Right>", forward_function)

		self.onclick()

	def is_paused(self):
		return self.button_playpause.photo == self.play_image

	def onclick(self, _event=...):
		if self.is_paused():
			self.animation.resume()
			self.button_playpause.photo = self.pause_image
		else:
			self.animation.pause()
			self.button_playpause.photo = self.play_image

		self.button_playpause.config(image=self.button_playpause.photo)
