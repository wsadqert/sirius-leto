from typing import Literal
from .animate import animate


def start(mode: Literal["basic", "windage"], plot_animation: bool = True, plot_alpha: bool = True) -> None:
	"""
	Function-wrapper for `src.lab1_pendulum.animate.animate(...)`.

	:param mode: Laboratory mode: classic (`basic`) or advanced (`windage`, taking into account air resistance).
	:param plot_animation: Flag determines whether the animation will be rendered.
	:param plot_alpha: Flag determines whether the graph of deviation angle versus time will be rendered.
	:return: None.
	"""

	if mode not in ["basic", "windage"]:
		raise ValueError(f"mode must be Literal[\"basic\", \"windage\"], but Literal[\"{mode}\"] provided")

	__import__(f"src.lab1_pendulum.{mode}.model")  # executing script to generate data

	animate(mode, plot_animation, plot_alpha)  # drawing requested plots
