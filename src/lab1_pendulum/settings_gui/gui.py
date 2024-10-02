import logging
import sys
from typing import Literal
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont

from src.general.checks import is_convertible, is_positive
from src.general.constants import g, pi
from src.lab1_pendulum.constants import CONFIG

from .tooltip import create_tooltip
from .custom_widgets import *
from .constants import *

__all__ = ["app", "start_gui"]


# types definitions
STATE: type = Literal["normal", "disabled"] | bool  # noqa UnionType is also `type`
COLOR: type = Literal["black", "gray"]
OBJECT2CHANGE: type = Literal['k', 'theory', 'extremums']
RAW_CONFIG: type = dict[str, str | bool]


def _change_state(name: OBJECT2CHANGE, new_state: STATE):
	"""
	Set the new state of lineedit and label `theory`.

	:param new_state: The new state of elements. If `bool`, 0 corresponds to `disabled`, 1 - to `normal`. Else, must be `normal` or `disabled`, other value will be rejected.
	:return: String representation of new color of text. Can take only 2 values: `gray` or `black`.
	"""
	allowed_string_values = STATE.__args__[0].__args__

	# processing incorrect data
	if name not in OBJECT2CHANGE.__args__:
		raise ValueError(f"Invalid object name: {name}. Name can be \"k\" or \"theory\"")
	if (new_state not in allowed_string_values) and not isinstance(new_state, bool):
		raise ValueError(f"Invalid new state: {new_state}. State can be \"normal\", \"disabled\" or boolean value")

	if name == 'k':
		object_ = lineedits['k']
	elif name == 'theory':
		object_ = checkboxes["theory"]
	elif name == 'extremums':
		object_ = checkboxes["extremums"]
	else:  # never will be executed
		raise Exception

	old_state = object_["state"]

	if isinstance(new_state, bool):
		new_state = allowed_string_values[1 - new_state]

	new_color: COLOR = ('gray', 'black')[new_state == 'normal']

	if new_state == old_state:
		return new_color

	object_.configure(state=new_state)
	if name == 'k':
		labels['k'].configure(fg=new_color)
		labels_units['кг/с'].configure(fg=new_color)
	elif name == 'theory':
		checkboxes["theory"].config(fg=new_color)
		if new_state == 'disabled':
			checkbox_variables["theory"].set(False)
	elif name == 'extremums':
		pass

	logging.debug(f"Changed `{name}` state from {old_state} to {new_state}.")

	return new_color


def _process_config(config: dict[str, ...] = None) -> CONFIG:
	"""
	Cast numbers to int/float, calculate constants, like `gamma` or `c1`.

	:param config: Dictionary with raw values from GUI.
	:return: Dictionary, containing information about a laboratory (see more in `datastore/lab1_pendulum/README_input.md`).
	"""
	if not config:
		return {}

	for key, value in config.items():
		if key in ("mode", "windage_method"):  # read strings
			cast_function = lambda x: x
		elif key == "fps":  # parse integer
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
		self.fps_combo_variable = tk.StringVar(value="60")

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

		for label_i in labels_h2_data:  # create h2's
			label_h2 = CustomLabel(
				text=label_i.text,
				font=self.font_18,
				align="left",
				place=label_i.place,
				size=labels_h2_size
			)
			labels_h2[label_i.name] = label_h2
		for label_i in labels_data:  # create labels
			# width_ = (120 if label_i.short_name == "frames_count_fps" else labels_size[0])

			label = CustomLabel(
				text=label_i.text + ' = ',
				font=self.font_10,
				align="right",
				place=label_i.place,
				size=labels_size
			)
			create_tooltip(label, label_i.hint)
			labels[label_i.name] = label
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
			elif name == "plot_alpha":
				command = self.__checkbox_plot_alpha_handler
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
		for lineedit_i in lineedits_data:  # creating lineedits
			current = tk.StringVar()

			lineedit = CustomLineEdit(
				font=self.font_10,
				align="right",
				place=lineedit_i.place,
				size=lineedits_size,
				variable=current,
				default_value=lineedit_i.default
			)

			lineedits[lineedit_i.name] = lineedit
			lineedit_variables[lineedit_i.name] = current

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

		self.fps_combo = ttk.Combobox(values=['30', '60', '90', '144'], textvariable=self.fps_combo_variable)
		self.fps_combo.place(x=380, y=290, width=lineedits_size[0], height=lineedits_size[1])

	def _check(self) -> bool:
		"""
		Checks correctness of data entered by user.

		:return: Boolean value, `True` if all entries filled correctly, `False` otherwise.
		"""
		ans = True

		for name, var in lineedit_variables.items():
			value = var.get()

			if name == "alpha_start":  # `alpha_start` may be negative
				checker_function = lambda x: is_convertible(x, float)
			elif name == "fps":  # it is counter, then it cannot be negative or float, only positive integer
				checker_function = lambda x: is_convertible(x, int)
			else:
				checker_function = is_positive

			if not checker_function(value):
				lineedits[name].config(highlightthickness=2, highlightbackground='red')  # add entry highlighting
				messagebox.showerror("Некорректный ввод",
				                     f"Поле {name} заполнено некорректно. ({name}=\"{value}\")\n\n"
				                     "Для справки: все поля должны содержать неотрицательные конечные вещественные числа, `k` - только положительное "
				                     "вещественное числа, `fps` - только положительное целое число.")
				ans = False
				logging.warning(f"Check lineedits failed: {name}")
			else:
				lineedits[name].config(highlightthickness=0)  # remove border

		value = int(self.fps_combo_variable.get())
		if 1 / int(value) < float(lineedit_variables["dt"].get()):
			# self.fps_combo.config(highlightthickness=2, highlightbackground='red') # add entry highlighting
			messagebox.showwarning("Некорректный ввод",
			                       f"Поле `fps` заполнено некорректно. (fps=\"{value}\")\n\n"
			                       f"При fps={value} интервал времени между соседними кадрами должен составлять {1_000_000 / value:.2f} мкс,"
			                       f" что меньше интервала между расчитываемыми шагами ({1_000_000 * float(lineedit_variables['dt'].get()):.2f} мкс). "
			                       f"Пожалуйста, уменьшите FPS до значения не более {1/float(lineedit_variables['dt'].get()):.0f}")
			ans = False
			logging.warning(f"Check lineedits failed: fps")
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

		_change_state('k', k_new_state)
		_change_state('theory', theory_new_state)

	def on_exit(self):
		logging.info("User attempted to leave")

		if messagebox.askyesno("Выход", "Вы уверены, что хотите выйти?"):
			self.destroy()
			logging.info("User confirmed, leaving...")

	def __checkbox_windage_handler(self) -> None:
		variable = checkbox_variables["windage"].get()

		if not variable:
			_change_state('theory', "normal")
			new_state = 'disabled'
		else:
			new_state = 'normal'

		self.__radio_handler()
		for entry in radios.values():
			entry.configure(state=new_state)

		if self.radio_variable.get() != 'realistic':
			new_color = _change_state('k', new_state)
			self.Label_windage_mode["fg"] = new_color

	def __checkbox_plot_alpha_handler(self) -> None:
		variable = checkbox_variables["plot_alpha"].get()
		if not variable:
			checkbox_variables["extremums"].set(False)
		_change_state("extremums", variable)

	def parse_input(self) -> RAW_CONFIG:
		"""
		Get data from entries, checkboxes, radio buttons and combo boxes in GUI.

		Numbers present as strings.
		Function does not provide any additional information, only data from elements of GUI.

		:return: Dictionary with raw values from GUI.
		"""
		config: CONFIG = {}

		is_windage = checkbox_variables['windage'].get()

		config['mode'] = 'windage' if is_windage else 'basic'
		config['windage_method'] = self.radio_variable.get() if is_windage else 'linear'

		# model
		config['calculate_theoretical'] = checkbox_variables['theory'].get()
		config['calculate_extremums'] = checkbox_variables['extremums'].get()
		config['dt'] = lineedit_variables['dt'].get()
		config['t_max'] = lineedit_variables['t_max'].get()

		# physics
		config['l'] = lineedit_variables['l'].get()
		config['alpha_start'] = str(float(lineedit_variables['alpha_start'].get()) * pi / 180)
		config['k'] = lineedit_variables['k'].get()
		config['m'] = lineedit_variables['m'].get()

		# rendering
		config['fps'] = self.fps_combo_variable.get()
		config['plot_animation'] = checkbox_variables['plot_animation'].get()
		config['plot_alpha'] = checkbox_variables['plot_alpha'].get()

		return config

	def start(self, _event=...) -> None:
		if not self._check():
			return

		self.destroy()

		config: RAW_CONFIG = self.parse_input()
		config: CONFIG = _process_config(config)

		self.config = config


app = App()


def start_gui() -> CONFIG:
	app.mainloop()
	return app.config
