from typing import Literal
from .animate import animate
from .model import model


def start(mode: Literal["basic", "windage"], plot_animation: bool = True, plot_alpha: bool = True, plot_theoretical: bool = False) -> None:
	"""
	Function-wrapper for `src.lab1_pendulum.animate.animate(...)`.

	:param mode: Laboratory mode: classic (`basic`) or advanced (`windage`, taking into account air resistance).
	:param plot_animation: Flag determines whether the animation will be rendered.
	:param plot_alpha: Flag determines whether the graph of deviation angle versus time will be rendered.
	:param plot_theoretical: Flag determines whether the theoretical dependence will be plotted.
	:return: None.
	"""

	if not plot_alpha and plot_theoretical:
		raise ValueError("cannot plot only theoretical dependence without model")

	if mode not in ["basic", "windage"]:
		raise ValueError(f"mode must be Literal[\"basic\", \"windage\"], but {mode = } provided")

	model(mode)
	animate(mode, plot_animation, plot_alpha, plot_theoretical)  # drawing requested plots
