import sys
import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
import configparser
from rich.traceback import install

from src.general.checks import *
from src.lab1_pendulum.constants import *

from .tooltip import CreateToolTip
from .custom_wingets import *
from .constants import *

install(show_locals=True, width=300)

__all__ = ["app", "start_gui"]


class App(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		self.title("Settings")

		screenwidth = self.winfo_screenwidth()
		screenheight = self.winfo_screenheight()
		alignstr = f"{width}x{height}+{(screenwidth - width) // 2}+{(screenheight - height) // 2}"

		self.geometry(alignstr)
		self.resizable(False, False)

		self.protocol("WM_DELETE_WINDOW", self.on_exit)

		self.font_10 = tkFont.Font(family='Times', size=10)
		self.font_18 = tkFont.Font(family='Times', size=18)
		self.font_33 = tkFont.Font(family='Times', size=33)

		self.radio_variable = tk.StringVar(value="linear")

		self.create_widgets()

	def on_exit(self):
		if messagebox.askyesno("Выход", "Вы уверены, что хотите выйти?"):
			self.destroy()
			sys.exit(0)

	def create_widgets(self) -> None:
		self.Label_title = CustomLabel(
			self,
			text="Настройки лаборатории",
			font=self.font_33,
			align="center",
			place=(0, 10),
			size=(527, 60)
		)

		for name, places in labels_h2_places.items():  # create h2's
			label_h2 = CustomLabel(
				self,
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
				self,
				text=name + ' = ',
				font=self.font_10,
				align="right",
				place=places,
				size=(width,
				      labels_size[1])
			)
			CreateToolTip(label, labels_hints[name])
			labels[name] = label
		for name, places in labels_units_places.items():  # create labels
			label_unit = CustomLabel(
				self,
				text=name,
				font=self.font_10,
				align="left",
				place=places,
				size=labels_units_size,
			)
			labels_units[name] = label_unit
		for name, (text, places) in radios_info.items():  # create radiobuttons
			radio = CustomRadiobutton(
				self,
				text=text,
				font=self.font_10,
				place=places,
				size=radios_size,
				variable=self.radio_variable,
				value=name,
				command=self.__disable_k_on_realistic
			)
			CreateToolTip(radio, radio_hints[name])
			radios[name] = radio
		for name, (text, places) in checkboxes_info.items():  # creating checkboxes
			current = tk.BooleanVar()

			if name == "windage":
				command = self.disable_windage_mode_selection
			else:
				command = lambda: None

			checkbox = CustomCheckBox(
				self,
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
				self,
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
			self,
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
		Button_start["command"] = self.start_command

	def __disable_k_on_realistic(self) -> None:
		if not checkbox_variables["windage"].get():
			return

		if self.radio_variable.get() == 'realistic':
			new_state = "disabled"
			new_color = "gray"
		else:
			new_state = "normal"
			new_color = "black"

		self.__config_k(new_state, new_color)

	def __config_k(self, new_state, new_color) -> None:
		lineedits['k'].configure(state=new_state)
		labels['k'].configure(fg=new_color)
		labels_units['кг/с'].configure(fg=new_color)

	def disable_windage_mode_selection(self) -> None:
		variable = checkbox_variables["windage"]

		if not variable.get():
			new_color = 'gray'
			new_state = 'disabled'
		else:
			new_color = 'black'
			new_state = 'normal'

		for entry in radios.values():
			entry.configure(state=new_state)

		if self.radio_variable.get() != 'realistic':
			self.__config_k(new_state, new_color)

		self.Label_windage_mode["fg"] = new_color

	def start_command(self) -> None:
		if not self.__check_lineedits():
			return

		config = configparser.ConfigParser()
		for section in ['model', 'physics', 'render']:
			config.add_section(section)

		is_windage = checkbox_variables['windage'].get()

		config['model']['mode'] = ('basic', 'windage')[is_windage]
		if is_windage:
			config['model']['windage_method'] = self.radio_variable.get()

		config['model']['calculate_theoretical'] = str(int(checkbox_variables['theory'].get()))
		config['model']['calculate_extremums'] = str(int(checkbox_variables['extremums'].get()))
		config['model']['dt'] = lineedit_variables['dt'].get()
		config['model']['t_max'] = lineedit_variables['t_max'].get()

		config['physics']['l'] = lineedit_variables['l'].get()
		config['physics']['alpha_start'] = lineedit_variables['alpha_start'].get()
		config['physics']['k'] = lineedit_variables['k'].get()
		config['physics']['m'] = lineedit_variables['m'].get()

		config['render']['render_dt'] = lineedit_variables['render_dt'].get()
		config['render']['frames_count_fps'] = lineedit_variables['frames_count_fps'].get()
		config['render']['plot_animation'] = str(int(checkbox_variables['plot_animation'].get()))
		config['render']['plot_alpha'] = str(int(checkbox_variables['plot_alpha'].get()))

		with open(datapath_input, 'w') as f:
			config.write(f)

		self.destroy()

	def __check_lineedits(self) -> bool:
		res = True
		for name, var in lineedit_variables.items():
			value = var.get()

			if name in tuple(lineedit_variables.keys())[-2:]:
				required_type = int
			else:
				required_type = float

			if name in ("alpha_start", "k"):
				checker_function = is_not_nan_inf
			else:
				checker_function = lambda value: is_positive(value, required_type)

			if not checker_function(value):
				lineedits[name].config(highlightthickness=2, highlightbackground='red')
				messagebox.showerror("Некорректный ввод",
				                     f"Поле {name} заполнено некорректно. ({name}=\"{value}\")\n\n"
				                     "Для справки: все поля должны содержать неотрицательные конечные вещественные числа, а последние 2 поля - только положительные целые числа")
				res = False
			else:
				lineedits[name].config(highlightthickness=0)
		return res


app = App()


def start_gui() -> None:
	app.mainloop()
