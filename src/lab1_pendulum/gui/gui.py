import logging
import sys
import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox

from src.general.constants import *
from src.general.checks import *

from .tooltip import create_tooltip
from .custom_wingets import *
from .constants import *


__all__ = ["app", "start_gui"]

STATE_TYPE = Literal["normal", "disable"]
COLOR_TYPE = Literal["black", "gray"]


class App(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("Settings")

		screenwidth = self.winfo_screenwidth()
		screenheight = self.winfo_screenheight()
		alignstr = f"{width}x{height}+{(screenwidth - width) // 2}+{(screenheight - height) // 2}"

		# setting up geometry
		self.geometry(alignstr)
		self.resizable(False, False)

		self.font_10 = tkFont.Font(family='Times', size=10)
		self.font_18 = tkFont.Font(family='Times', size=18)
		self.font_33 = tkFont.Font(family='Times', size=33)

		self.radio_variable = tk.StringVar(value="linear")

		self.create_widgets()

		# handlers
		self.protocol("WM_DELETE_WINDOW", self.on_exit)
		self.bind('<Return>', self.start)

	def create_widgets(self) -> None:
		self.Label_title = CustomLabel(
			text="Настройки лаборатории",
			font=self.font_33,
			align="center",
			place=(0, 10),
			size=(527, 60)
		)

		for name, places in labels_h2_places.items():  # create h2's
			label_h2 = CustomLabel(
				text=name,
				font=self.font_18,
				align="left",
				place=places,
				size=labels_h2_size
			)
			labels_h2[name] = label_h2
		for name, places in labels_places.items():  # create labels
			width = (120 if name == "frames_count_fps" else labels_size[0])

			label = CustomLabel(
				text=name + ' = ',
				font=self.font_10,
				align="right",
				place=places,
				size=(width,
				      labels_size[1])
			)
			create_tooltip(label, labels_hints[name])
			labels[name] = label
		for name, places in labels_units_places.items():  # create labels
			label_unit = CustomLabel(
				text=name,
				font=self.font_10,
				align="left",
				place=places,
				size=labels_units_size,
			)
			labels_units[name] = label_unit
		for name, (text, places) in radios_info.items():  # create radiobuttons
			radio = CustomRadioButton(
				text=text,
				font=self.font_10,
				place=places,
				size=radios_size,
				variable=self.radio_variable,
				value=name,
				command=self.__radio_handler
			)
			create_tooltip(radio, radio_hints[name])
			radios[name] = radio
		for name, (text, places) in checkboxes_info.items():  # creating checkboxes
			current = tk.BooleanVar()

			if name == "windage":
				command = self.__checkbox_windage_handler
			else:
				command = lambda: None

			checkbox = CustomCheckBox(
				text=text,
				font=self.font_10,
				place=places,
				command=command,
				variable=current,
				size=checkboxes_size
			)

			checkboxes[name] = checkbox
			checkbox_variables[name] = current
		for name, places in lineedits_places.items():  # creating lineedits
			current = tk.StringVar()

			lineedit = CustomLineEdit(
				font=self.font_10,
				align="right",
				place=places,
				size=lineedits_size,
				variable=current,
				default_value=lineedits_defaults[name]
			)

			lineedits[name] = lineedit
			lineedit_variables[name] = current

		self.Label_windage_mode = CustomLabel(
			text="Зависимость сопротивления\nвоздуха от скорости",
			font=self.font_10,
			align="left",
			place=(30, 260),
			size=(240, 40)
		)

		Button_start = tk.Button(self)
		Button_start["anchor"] = "center"
		Button_start["bg"] = "#00b800"
		Button_start["font"] = self.font_33
		Button_start["fg"] = "#ffffff"
		Button_start["justify"] = "center"
		Button_start["text"] = "Запуск!"
		Button_start["relief"] = "flat"
		Button_start.place(
			x=button_place[0],
			y=button_place[1],
			width=button_size[0],
			height=button_size[1]
		)
		Button_start["command"] = self.start

		CustomLabel(
			text="Press Enter to continue",
			font=self.font_10,
			align='left',
			place=(30, 430),
			size=(200, labels_size[1]),
			fg="gray"
		)

	def __config_k(self, new_state: STATE_TYPE | bool) -> COLOR_TYPE:
		"""
		Sets the new state of lineedit and label `k`.

		:param new_state: The new state of elements. If `bool`, 0 corresponds to `disabled`, 1 - to `normal`. Else, must be `normal` or `disabled`, other value will be rejected.
		:return: String representation of new color of text. Can take only 2 values: `gray` or `black`.
		"""
		assert (new_state in STATE_TYPE.__args__) or isinstance(new_state, bool)

		old_state = new_state

		if isinstance(new_state, bool):
			new_state = STATE_TYPE.__args__[1-new_state]

		new_color = ('gray', 'black')[new_state == 'normal']

		lineedits['k'].configure(state=new_state)
		labels['k'].configure(fg=new_color)
		labels_units['кг/с'].configure(fg=new_color)

		logging.info(f"Changed `k` state from {old_state} to {new_state}.")

		return new_color

	def __config_theory(self, new_state: STATE_TYPE) -> COLOR_TYPE:
		"""
		Sets the new state of lineedit and label `theory`.

		:param new_state: The new state of elements. If `bool`, 0 corresponds to `disabled`, 1 - to `normal`. Else, must be `normal` or `disabled`, other value will be rejected.
		:return: String representation of new color of text. Can take only 2 values: `gray` or `black`.
		"""
		assert (new_state in STATE_TYPE.__args__) or isinstance(new_state, bool)

		old_state = new_state

		if isinstance(new_state, bool):
			new_state = STATE_TYPE.__args__[1-new_state]

		new_color = ('gray', 'black')[new_state == 'normal']

		checkboxes["theory"].config(state=new_state, fg=new_color)
		if new_state == 'disabled':
			checkbox_variables["theory"].set(False)

		logging.info(f"Changed `k` state from {old_state} to {new_state}.")

		return new_color

	def __check_lineedits(self) -> bool:
		"""
		Checks correctness of data entered byy user.

		:return: boolean value, `True` if all entries filled correctly, `False` otherwise.
		"""
		ans = True

		for name, var in lineedit_variables.items():
			value = var.get()

			if name == "alpha_start":  # `alpha_start` may be negative
				checker_function = lambda x: is_convertible(x, float)
			elif name in ("render_dt", "frames_count_fps"):  # there are counters, then they cannot be negative or float, only positive integers
				checker_function = lambda x: is_convertible(x, int)
			else:
				checker_function = is_positive

			if not checker_function(value):
				lineedits[name].config(highlightthickness=2, highlightbackground='red')  # add entry highlighting
				messagebox.showerror("Некорректный ввод",
				                     f"Поле {name} заполнено некорректно. ({name}=\"{value}\")\n\n"
				                     "Для справки: все поля должны содержать неотрицательные конечные вещественные числа, `k` - только положительные действительные числа, `render_dt` и `frames_count_fps` - только положительные целые числа.")
				ans = False
				logging.warning(f"Check lineedits failed: {name}")
			else:
				lineedits[name].config(highlightthickness=0)  # remove border
		else:
			pass
		return ans

	# EVENT HANDLERS

	def __radio_handler(self) -> None:
		if not checkbox_variables["windage"].get():
			return

		selection = self.radio_variable.get()

		if selection == 'realistic':
			k_new_state = "disabled"
		else:
			k_new_state = "normal"

		if selection in ("realistic", "quadratic"):
			theory_new_state = "disabled"
		else:
			theory_new_state = "normal"

		self.__config_k(k_new_state)
		self.__config_theory(theory_new_state)

	def on_exit(self):
		logging.info("User attempted to leave")

		if messagebox.askyesno("Выход", "Вы уверены, что хотите выйти?"):
			self.destroy()
			logging.info("User confirmed, leaving...")
			sys.exit(0)

	def __checkbox_windage_handler(self) -> None:
		variable = checkbox_variables["windage"].get()

		if not variable:
			self.__config_theory("normal")
		self.__radio_handler()

		if not variable:
			new_state = 'disabled'
			new_color = 'gray'
		else:
			new_state = 'normal'
			new_color = 'black'

		for entry in radios.values():
			entry.configure(state=new_state)

		if self.radio_variable.get() != 'realistic':
			self.__config_k(new_state)

		self.Label_windage_mode["fg"] = new_color

	def __process_config(self, config) -> dict[str, ...]:
		for key, value in config.items():
			if key in ("mode", "windage_method"):  # read strings
				cast_function = lambda x: x
			elif key in ("render_dt", "frames_count_fps"):  # parse integer
				cast_function = int
			elif key in ("calculate_theoretical", "calculate_extremums", "plot_animation", "plot_alpha"):  # parse boolean
				cast_function = lambda x: x
			else:  # parse float
				cast_function = float

			config[key] = cast_function(value)

		if config['mode'] == 'basic':
			config['k'] = 0

		# see README.md for description
		config['gamma'] = config['k'] / (2 * config['m'])
		config['beta'] = config['gamma'] ** 2 - g / config['l']
		config['c1'] = config['gamma'] * config['dt']
		config['c2'] = g * config['dt'] ** 2 / config['l']

		return config

	def start(self, event=...) -> None:
		if not self.__check_lineedits():
			return

		config = {}

		is_windage = checkbox_variables['windage'].get()

		config['mode'] = ('basic', 'windage')[is_windage]
		if is_windage:
			config['windage_method'] = self.radio_variable.get()

		# model
		config['calculate_theoretical'] = checkbox_variables['theory'].get()
		config['calculate_extremums']   = checkbox_variables['extremums'].get()
		config['dt']    = lineedit_variables['dt'].get()
		config['t_max'] = lineedit_variables['t_max'].get()

		# physics
		config['l']           = lineedit_variables['l'].get()
		config['alpha_start'] = lineedit_variables['alpha_start'].get()
		config['k']           = lineedit_variables['k'].get()
		config['m']           = lineedit_variables['m'].get()

		# rendering
		config['render_dt']        = lineedit_variables['render_dt'].get()
		config['frames_count_fps'] = lineedit_variables['frames_count_fps'].get()
		config['plot_animation'] = checkbox_variables['plot_animation'].get()
		config['plot_alpha']     = checkbox_variables['plot_alpha'].get()

		self.destroy()

		config = self.__process_config(config)
		self.config = config


app = App()


def start_gui() -> dict[str, dict[str, ...]]:
	app.mainloop()
	return app.config
