from typing import Literal
from .animate import animate


def start(mode: Literal["basic", "windage"], plot_animation: bool = True, plot_alpha: bool = True):
	if mode not in ["basic", "windage"]:
		raise ValueError
	__import__(f"src.lab1_pendulum.{mode}.model")

	animate(mode, plot_animation, plot_alpha)
