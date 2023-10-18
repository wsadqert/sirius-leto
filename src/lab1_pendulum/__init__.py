from .animate import animate
from .model import model
from .constants import *


def start(plot_animation: bool = True, plot_alpha: bool = True, plot_theoretical: bool = False) -> None:
	"""
	Wrapper for `src.lab1_pendulum.animate.animate(...)`.

	:param plot_animation: Flag determines whether the animation will be rendered.
	:param plot_alpha: Flag determines whether the graph of deviation angle versus time will be rendered.
	:param plot_theoretical: Flag determines whether the theoretical dependence will be plotted.
	:return: None.
	"""

	if mode not in MODE.__args__:
		raise ValueError(f"mode must be one of {MODE.__args__} but {mode = } is provided")

	model()
	animate(plot_animation, plot_alpha, plot_theoretical)  # drawing requested plots
