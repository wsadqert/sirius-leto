from typing import Literal
from .animate import animate


def start(mode: Literal["basic", "windage"], plot_animation: bool = True, plot_alpha: bool = True):
	"""
	Function-wrapper for

	:param mode: режим лаборатории: классический или с учётом сопротивления воздуха.
	:param plot_animation: флаг, определяющий, будет ли рендериться анимация.
	:param plot_alpha: флаг, определяющий, будет ли рендериться график угла отклонения от времени.
	:return:
	"""

	if mode not in ["basic", "windage"]:
		raise ValueError(f"mode must be Literal[\"basic\", \"windage\"], but Literal[\"{mode}\"] provided")

	__import__(f"src.lab1_pendulum.{mode}.model")  # executing script to generate data

	animate(mode, plot_animation, plot_alpha)  # drawing requested plots
