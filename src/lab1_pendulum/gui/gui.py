import tkinter as tk
import tkinter.font as tkFont
from tkinter.messagebox import showerror
from rich.traceback import install

from .ToolTip import CreateToolTip
from .custom_wingets import *
from src.general.checks import is_non_negative

install(show_locals=True, width=300)


class App:
	def __init__(self, root):
		root.title("Settings")
		width = 527
		height = 446
		screenwidth = root.winfo_screenwidth()
		screenheight = root.winfo_screenheight()
		alignstr = f"{width}x{height}+{(screenwidth - width) // 2}+{(screenheight - height) // 2}"
		root.geometry(alignstr)
		root.resizable(False, False)

		self.__font_10 = tkFont.Font(family='Times', size=10)
		self.__font_18 = tkFont.Font(family='Times', size=18)
		self.__font_33 = tkFont.Font(family='Times', size=33)

		self.__labels_h2_info = {
			"Настройки модели": (40, 80),
			"Рендер": (290, 250),
			"Физика": (290, 80)
		}
		self.__labels_h2_size = (200, 35)

		self.__labels_info = {
			"dt": (20, 120),
			"t_max": (20, 150),
			"l": (280, 120),
			"alpha_start": (280, 150),
			"k": (280, 180),
			"m": (280, 210),
			"render_dt": (280, 290),
			"frames_count_fps": (260, 320)
		}
		self.__labels_size = (100, 25)

		self.__labels_units_info = {
			"с ": (200, 120),
			"с": (200, 150),
			"м": (460, 120),
			"рад": (460, 150),
			"кг/с": (460, 180),
			"кг": (460, 210),
		}
		self.__labels_units_size = (30, 25)

		self.__lineedits_info = {
			"dt": (120, 120),
			"t_max": (120, 150),
			"l": (380, 120),
			"alpha_start": (380, 150),
			"k": (380, 180),
			"m": (380, 210),
			"render_dt": (380, 290),
			"frames_count_fps": (380, 320),
		}
		self.__lineedits_size = (75, 25)
		self.__lineedit_variables = dict()
		self.lineedits = {}

		self.__checkboxes_info = {
			"theory": ("Расчитывать аналитическое решение", (40, 190)),
			"windage": ("Учитывать сопротивление воздуха", (40, 220)),
			"extremums": ("Отображать пики на графике", (280, 350)),
		}
		self.__checkboxes_size = (230, 30)
		self.__checkbox_variables = dict()

		self.__radios_info = {
			"kv": (40, 300),
			"kv^2": (130, 300),
			"реалистично": (40, 320)
		}
		self.__radios_size = (100, 25)
		self.__radio_variable = tk.StringVar(value="kv")
		self.radios = {}

		self.create_widgets()

	def create_widgets(self):
		Label_title = CustomLabel(
			root,
			text="Настройки лаборатории",
			font=self.__font_33,
			align="center",
			place=(0, 10),
			size=(527, 60)
		)

		for name, places in self.__labels_h2_info.items():  # create h2's
			Label_h2 = CustomLabel(
				root,
				text=name,
				font=self.__font_18,
				align="left",
				place=places,
				size=self.__labels_h2_size
			)
		for name, places in self.__labels_info.items():  # create labels
			width = (120 if name == "frames_count_fps" else self.__labels_size[0])

			CustomLabel(
				root,
				text=name + ' = ',
				font=self.__font_10,
				align="right",
				place=places,
				size=(width,
				      self.__labels_size[1])
			)
		for name, places in self.__labels_units_info.items():  # create labels
			CustomLabel(
				root,
				text=name,
				font=self.__font_10,
				align="left",
				place=places,
				size=self.__labels_units_size,
			)
		for name, places in self.__radios_info.items():
			radio = CustomRadiobutton(
				root,
				text=name,
				font=self.__font_10,
				place=places,
				size=self.__radios_size,
				variable=self.__radio_variable
			)
			self.radios[name] = radio
		for name, (text, place) in self.__checkboxes_info.items():
			current = tk.BooleanVar()

			if name == "windage":
				command = self.disable_windage_mode_selection
			else:
				command = lambda: None

			CustomCheckBox(
				root,
				text=text,
				font=self.__font_10,
				place=place,
				command=command,
				variable=current,
				size=self.__checkboxes_size
			)

			self.__checkbox_variables[name] = current
		for name, places in self.__lineedits_info.items():
			current = tk.StringVar()

			lineedit = CustomLineEdit(
				root,
				font=self.__font_10,
				align="right",
				place=places,
				size=self.__lineedits_size,
				variable=current
			)

			self.lineedits[name] = lineedit
			self.__lineedit_variables[name] = current

		self.Label_windage_mode = CustomLabel(
			root,
			text="Зависимость сопротивления\nвоздуха от скорости",
			font=self.__font_10,
			align="left",
			place=(30, 260),
			size=(240, 40)
		)

		Button_start = tk.Button(root)
		Button_start["anchor"] = "center"
		Button_start["bg"] = "#00b800"
		Button_start["font"] = self.__font_18
		Button_start["fg"] = "#ffffff"
		Button_start["justify"] = "center"
		Button_start["text"] = "Запуск!"
		Button_start["relief"] = "flat"
		Button_start.place(x=30, y=370, width=192, height=50)
		Button_start["command"] = self.start_command

	def disable_windage_mode_selection(self):
		variable = self.__checkbox_variables["windage"]

		if not variable.get():
			self.Label_windage_mode["fg"] = 'gray'
			new_state = 'disabled'
		else:
			self.Label_windage_mode["fg"] = 'black'
			new_state = 'normal'

		for entry in self.radios.values():
			entry.configure(state=new_state)

	def start_command(self):
		if self.__check_lineedits():
			root.destroy()

	def __check_lineedits(self) -> bool:
		res = True
		for name, var in self.__lineedit_variables.items():
			value = var.get()
			if not is_non_negative(value):
				self.lineedits[name].config(highlightthickness=2, highlightbackground='red')
				showerror("Некорректный ввод",
				          f"Поле {name} заполнено некорректно. ({name}=\"{value}\")\n\n"
				          f"Для справки: все поля должны содержать конечные вещественные числа")
				res = False
			else:
				self.lineedits[name].config(highlightthickness=0)
		return res


root = tk.Tk()
app = App(root)
root.mainloop()
