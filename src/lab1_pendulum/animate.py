import logging
from typing import Sequence

import matplotlib as mpl
import matplotlib.artist
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

from src.lab1_pendulum.constants import datapath_model, figsize, pendulum_axis_x, pendulum_axis_y, plot_lims, text_y
from src.general.constants import sleep, real_time, pi
from src.general.calculations import pol2cart


def _animation_step(frame: int, alpha_array: Sequence[float | np.float64], config: dict[str, ...]) -> tuple[mpl.artist.Artist, ...]:
	"""
	Get data from pre-calculated array and change coordinates of points and a line.

	:param frame: Number of animation frame.
	:param alpha_array: Array (list/ or other sequence-like object) with pendulum deflection angles.
	:param config: Dictionary, containing information about a laboratory (see more in `datastore/lab1_pendulum/README_input.md`).
	:return: Tuple from `matplotlib.artist.Artist` objects to redraw.
	"""
	global time_previous_frame, pendulum_line, pendulum_point, time_text, n  # noqa - variables are defined in `animate()`

	for i in config.keys():
		globals()[i] = config[i]

	# calculating current time inside the simulation
	time = frame / fps
	data_item_index = round(time / dt)

	# fps counting
	# print(f'\rfps = {frames_count_fps / (t1 - time_previous_frame):.2f}', end='')  # printing fps value

	if frame == 0:
		time_previous_frame = real_time()

	# if animation was ended, but was not closed, continue to draw exciting Artists without changing
	if data_item_index >= n:
		return pendulum_line, pendulum_point, time_text

	# by default, angle is in [0; 2×pi], but for correct rendering we need angle in [-pi/2; 3/4×pi],
	# so we subtract pi/2 from each alpha value
	alpha: float = alpha_array[data_item_index] - pi / 2

	# converting polar coordinates (l, alpha) to cartesian (x, y)
	x, y = pol2cart(l, alpha)

	# pendulum axis's coordinates is not always (0, 0),
	# so we need to add (pendulum_axis_x, pendulum_axis_y) to get (x, y)
	x += pendulum_axis_x
	y += pendulum_axis_y

	# updating coordinates on plot
	pendulum_point.set_data([x], [y])
	pendulum_line.set_data([pendulum_axis_x, x], [pendulum_axis_y, y])

	# limiting fps
	"""
	Why can't we use `interval` property of `FuncAnimation` class to limit FPS?

	In the beginning of execution we don't know the exact time to render one frame. If we set interval of animation to 1/fps, 
	real interval will be greater, and will be determined by computer performance. Therefore, the real fps will be lower.

	So, if we will determine an interval dynamically, there will not be this problem.
	"""
	t1 = real_time()
	if t1 - time_previous_frame < 1 / fps:
		sleep(1 / fps - (t1 - time_previous_frame))  # 1/fps is time between two consecutive frames
	time_previous_frame = real_time()

	# updating stopwatch (format “0.00 s”)
	if frame != 0:
		time_text.set_text(rf"${time:.2f}\,s$")

	return pendulum_line, pendulum_point, time_text


def animate(config: dict[str, ...]) -> None:  # is_in_demo: bool = False
	"""
	Gets pre-calculated data from `datapath_model` and plots it.

	:param config: Dictionary, containing information about a laboratory (see more in `datastore/lab1_pendulum/README_input.md`).
	"""
	global n, pendulum_line, pendulum_point, time_text  # noqa - variables will be defined below

	for i in config.keys():
		globals()[i] = config[i]

	logging.info("Starting setting up matplotlib")

	with open(datapath_model) as f:  # reading data generated by `model.py`
		n = int(f.readline().strip())

		time_array = [float(i) for i in f.readline().strip().split()]  # noqa double space
		alpha_array = [float(i) for i in f.readline().strip().split()]

		if calculate_extremums:
			extremums_x = [float(i) for i in f.readline().strip().split()]
			extremums_y = [float(i) for i in f.readline().strip().split()]

		if calculate_theoretical:
			theoretical_alpha_array = [float(i) for i in f.readline().strip().split()]
			if calculate_extremums:
				extremums_theory_x = [float(i) for i in f.readline().strip().split()]
				extremums_theory_y = [float(i) for i in f.readline().strip().split()]

	mpl.rcParams['mathtext.fontset'] = 'cm'
	mpl.rcParams['figure.figsize'] = (figsize, figsize)

	if plot_animation:  # show animation
		fig, _ = plt.subplots()
		plt.title("Numerical model of a pendulum")
		plt.grid(True, linestyle='--')
		plt.xlabel(r'$x, m$', fontsize=13)
		plt.ylabel(r'$y, m$', fontsize=13)
		plt.xlim(-plot_lims * l, plot_lims * l)
		plt.ylim(-plot_lims * l, plot_lims * l)

		pendulum_line, = plt.plot([], [], linewidth=2, color='blue')
		pendulum_axis, = plt.plot([pendulum_axis_x], [pendulum_axis_y], marker='o', markersize=5, color='red')  # noqa, required for animation
		pendulum_point, = plt.plot([], [], marker='o', markersize=5, color='red')
		time_text = plt.text(0, text_y * l, "", fontsize=20)
		animation = FuncAnimation(fig,  # noqa - do not remove assigning to variable, it breakes animation!
		                          func=_animation_step,
		                          fargs=(alpha_array, config),  # , is_in_demo,),
		                          interval=0,
		                          frames=n,
		                          blit=True,
		                          repeat=False,
		                          cache_frame_data=True)

	if plot_alpha:  # show angle plot
		plt.figure()
		plt.grid(True, linestyle='--')
		plt.xlabel(r"$t, s$", fontsize=13)
		plt.ylabel(r"$\alpha, rad$", fontsize=13)
		plt.axhline(y=0, color='black', ls='--')

		color = plt.plot(time_array, alpha_array, label="simulation")[0].get_color()
		if calculate_extremums:
			plt.plot(extremums_x, extremums_y, 'o', color=color)  # points
			for i in range(len(extremums_x)):  # vertical dash lines
				plt.axvline(extremums_x[i], ymin=-plot_lims, ymax=plot_lims, color=color, linewidth=1, ls='--')

		if calculate_theoretical:
			color = plt.plot(time_array, theoretical_alpha_array, label="theory")[0].get_color()
			if calculate_extremums:
				plt.plot(extremums_theory_x, extremums_theory_y, 'o', color=color)
				for i in range(len(extremums_theory_x)):  # vertical dash lines
					plt.axvline(extremums_theory_x[i], ymin=-plot_lims, ymax=plot_lims, color=color, linewidth=1, ls='--')

	plt.legend(loc="upper right")
	logging.info("Matplotlib set up, starting animation")

	plt.show()
