import logging
from typing import Sequence
import numpy as np

import tkinter as tk
import matplotlib as mpl
import matplotlib.artist
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from src.lab1_pendulum.constants import CONFIG, DATASET, figsize, pendulum_axis_x, pendulum_axis_y, plot_lims, text_y
from src.lab1_pendulum.plotting_gui.play_pause_window import PlayPauseWindow
from src.general.constants import sleep, real_time, pi
from src.general.calculations import pol2cart

frame = 0


def _animation_step(_frame: int, alpha_array: Sequence[float | np.float64], config: dict[str, ...], realtime_flag=True) -> tuple[mpl.artist.Artist, ...]:
	"""
	Get data from pre-calculated array and change coordinates of points and a line.

	:param frame: Number of animation frame.
	:param alpha_array: Array (list/ or other sequence-like object) with pendulum deflection angles.
	:param config: Dictionary, containing information about a laboratory (see more in `datastore/lab1_pendulum/README_input.md`).
	:return: Tuple from `matplotlib.artist.Artist` objects to redraw.
	"""
	global time_previous_frame, pendulum_line, pendulum_point, time_text, n, frame  # noqa - variables are defined in `animate()`

	dt = config['dt']
	l = config['l']
	fps = config['fps']

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

	# Why can't we use `interval` property of `FuncAnimation` class to limit FPS?
	#
	# In the beginning of execution we don't know the exact time to render one frame. If we set interval of animation to 1/fps,
	# real interval will be greater, and will be determined by computer performance. Therefore, the real fps will be lower.
	#
	# So, if we will determine an interval dynamically, there will not be this problem.

	if realtime_flag:
		t1 = real_time()
		if t1 - time_previous_frame < 1 / fps:
			sleep(1 / fps - (t1 - time_previous_frame))  # 1/fps is time between two consecutive frames
		time_previous_frame = real_time()

	# updating stopwatch (format “0.00 s”)
	if frame != 0:
		time_text.set_text(rf"${time:.2f}\,s$")

	frame += 1

	return pendulum_line, pendulum_point, time_text


def back(_event=..., dtime=1):
	global frame, fps

	frame = max(0, frame - dtime * fps)


def forward(_event=..., dtime=1):
	global frame, n, fps

	frame = min(n, frame + dtime * fps)


def animate(dataset: DATASET, config: CONFIG) -> None:  # is_in_demo: bool = False
	"""
	Gets pre-calculated data from `datapath_model` and plots it.

	:param config: Dictionary, containing information about a laboratory (see more in `datastore/lab1_pendulum/README_input.md`).
	"""
	global n, pendulum_line, pendulum_point, time_text, alpha_array, fps  # noqa - variables will be defined below

	logging.debug("Extracting data from config")

	# extracting values from config
	calculate_extremums = config['calculate_extremums']
	calculate_theoretical = config['calculate_theoretical']
	plot_alpha = config['plot_alpha']
	plot_animation = config['plot_animation']
	l = config['l']
	fps = config['fps']

	logging.debug("Extracting data from dataset")

	n = dataset['n']
	time_array = dataset['time_array']
	alpha_array = dataset['alpha_array']

	if calculate_extremums:
		print(sorted(dataset['extremums_x']))
		extremums_x = dataset['extremums_x']
		extremums_y = dataset['extremums_y']
	if calculate_theoretical and calculate_extremums:
		extremums_theory_x = dataset['extremums_theory_x']
		extremums_theory_y = dataset['extremums_theory_y']
	if calculate_theoretical:
		theoretical_alpha_array = dataset['theoretical_alpha_array']

	# setting up tkinter
	if plot_animation:
		logging.info("Creating tkinter window")
		root = tk.Tk()
		root.wm_title("Main window")

	logging.info("Creating matplotlib subplots")

	mpl.rcParams['mathtext.fontset'] = 'cm'

	# setting up subplots
	if plot_animation and plot_alpha:
		fig, (ax_anim, ax_plot) = plt.subplots(1, 2, figsize=(2 * figsize, figsize), subplot_kw=dict(box_aspect=1))
	elif plot_animation:
		fig, ax_anim = plt.subplots(figsize=(figsize, figsize), subplot_kw=dict(box_aspect=1))
	elif plot_alpha:
		fig, ax_plot = plt.subplots(figsize=(figsize, figsize), subplot_kw=dict(box_aspect=1))
	else:
		return

	# show animation
	if plot_animation:
		logging.debug("Setting up subplot with animation")

		ax_anim.set_title("Pendulum real-time animation")
		ax_anim.grid(True, linestyle='--')
		ax_anim.set_xlabel(r'$x, m$', fontsize=13)
		ax_anim.set_ylabel(r'$y, m$', fontsize=13)
		ax_anim.set_xlim(-plot_lims * l, plot_lims * l)
		ax_anim.set_ylim(-plot_lims * l, plot_lims * l)

		pendulum_line, = ax_anim.plot([], [], linewidth=2, color='blue')
		pendulum_axis, = ax_anim.plot([pendulum_axis_x], [pendulum_axis_y], marker='o', markersize=5, color='red')  # noqa, required for animation
		pendulum_point, = ax_anim.plot([], [], marker='o', markersize=5, color='red')
		time_text = ax_anim.text(0, text_y * l, "", fontsize=20)
		animation = FuncAnimation(fig,  # noqa - do not remove assigning to variable, it breakes animation!
		                          func=_animation_step,
		                          fargs=(alpha_array, config),
		                          interval=0,
		                          # frames=int(config['t_max'] * config['fps']),
		                          blit=True,
		                          repeat=False,
		                          cache_frame_data=True)

		# logging.info("Saving animation as gif")
		# animation.save('ani.gif', metadata=dict(artist='Me'), fps=fps)

		if plot_animation:
			logging.info("Setting up tkinter control buttons")

			canvas = FigureCanvasTkAgg(fig, master=root)
			canvas.draw()

			toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
			toolbar.update()

			PlayPauseWindow(root, animation, back, forward)

			toolbar.pack(side=tk.BOTTOM, fill=tk.X)
			canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

	# show angle plot
	if plot_alpha:
		logging.debug("Setting up subplot with chart")

		ax_plot.set_title("some plot ^_^")
		ax_plot.grid(True, linestyle='--')
		ax_plot.set_xlabel(r"$t, s$", fontsize=13)
		ax_plot.set_ylabel(r"$\alpha, rad$", fontsize=13)
		ax_plot.axhline(y=0, color='black', ls='--')

		logging.debug("Drawing extremums")

		color = ax_plot.plot(time_array, alpha_array, label="simulation")[0].get_color()
		if calculate_extremums:
			ax_plot.plot(extremums_x, extremums_y, 'o', color=color)  # points
			for i in range(len(extremums_x)):  # vertical dash lines
				ax_plot.axvline(extremums_x[i], ymin=-plot_lims, ymax=plot_lims, color=color, linewidth=1, ls='--')

		if calculate_theoretical:
			color = ax_plot.plot(time_array, theoretical_alpha_array, label="theory")[0].get_color()
			if calculate_extremums:
				ax_plot.plot(extremums_theory_x, extremums_theory_y, 'o', color=color)
				for i in range(len(extremums_theory_x)):  # vertical dash lines
					ax_plot.axvline(extremums_theory_x[i], ymin=-plot_lims, ymax=plot_lims, color=color, linewidth=1, ls='--')

	plt.legend(loc="upper right")

	# starting mainloop
	if plot_animation:
		logging.info("Starting tkinter mainloop")
		root.mainloop()
	else:
		logging.info("Starting matplotlib mainloop")
		plt.show()
