import tkinter as tk
import tkinter.font as tkFont
from tkinter.messagebox import showerror
import configparser
from rich.traceback import install

from .ToolTip import CreateToolTip
from .custom_wingets import *
from src.general.checks import is_positive

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
		self.__labels_hints = {
			"dt": "Шаг симуляции. Должен быть как \nминимум на 3 порядка меньше `t_max`",
			"t_max": "Максимальное время симуляции",
			"l": "Длина маятника",
			"alpha_start": "Начальный угол отклонения маятника \nот положения равновесия",
			"k": "Коэффициент сопротивления воздуха",
			"m": "Масса груза на конце маятника",
			"render_dt": "Количество тактов, через которые \nбудет обновляться изображение на экране",
			"frames_count_fps": "Количество кадров, которые \nиспользуются для расчёта FPS"
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
			"linear": ("kv", (40, 300)),
			"quadratic": ("kv^2", (130, 300)),
			"realistic": ("реалистично", (40, 320))
		}
		self.__radio_hints = {
			"linear": "Линейная зависимость силы \nсопротивления от скорости",
			"quadratic": "Квадратичная зависимость силы \nсопротивления от скорости",
			"realistic": "Наиболее реалистичная зависимость, \nполученная с помощью численного моделирования \nв профессиональных пакетах"
		}
		self.__radios_size = (100, 25)
		self.__radio_variable = tk.StringVar(value="linear")
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

			label = CustomLabel(
				root,
				text=name + ' = ',
				font=self.__font_10,
				align="right",
				place=places,
				size=(width,
				      self.__labels_size[1])
			)
			CreateToolTip(label, self.__labels_hints[name])
		for name, places in self.__labels_units_info.items():  # create labels
			CustomLabel(
				root,
				text=name,
				font=self.__font_10,
				align="left",
				place=places,
				size=self.__labels_units_size,
			)
		for name, (text, places) in self.__radios_info.items():
			radio = CustomRadiobutton(
				root,
				text=text,
				font=self.__font_10,
				place=places,
				size=self.__radios_size,
				variable=self.__radio_variable,
				value=name
			)
			CreateToolTip(radio, self.__radio_hints[name])
			self.radios[name] = radio
		for name, (text, places) in self.__checkboxes_info.items():
			current = tk.BooleanVar()

			if name == "windage":
				command = self.disable_windage_mode_selection
			else:
				command = lambda: None

			CustomCheckBox(
				root,
				text=text,
				font=self.__font_10,
				place=places,
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
		if not self.__check_lineedits():
			return

		config = configparser.ConfigParser()
		for section in ['model', 'physics', 'render']:
			config.add_section(section)

		is_windage = self.__checkbox_variables['windage'].get()

		config['model']['mode'] = ('basic', 'windage')[is_windage]
		if is_windage:
			config['model']['windage_method'] = self.__radio_variable.get()

		config['model']['calculate_theoretical'] = str(int(self.__checkbox_variables['theory'].get()))
		config['model']['calculate_extremums'] = str(int(self.__checkbox_variables['extremums'].get()))
		config['model']['dt'] = self.__lineedit_variables['dt'].get()
		config['model']['t_max'] = self.__lineedit_variables['t_max'].get()

		config['physics']['l'] = self.__lineedit_variables['l'].get()
		config['physics']['alpha_start'] = self.__lineedit_variables['alpha_start'].get()
		config['physics']['k'] = self.__lineedit_variables['k'].get()
		config['physics']['m'] = self.__lineedit_variables['m'].get()

		config['render']['render_dt'] = self.__lineedit_variables['render_dt'].get()
		config['render']['frames_count_fps'] = self.__lineedit_variables['frames_count_fps'].get()

		with open('example.ini', 'w') as f:
			config.write(f)

		root.destroy()

	def __check_lineedits(self) -> bool:
		res = True
		for name, var in self.__lineedit_variables.items():
			value = var.get()

			print(name)

			if name in tuple(self.__lineedit_variables.keys())[-2:]:
				required_type = int
			else:
				required_type = float

			if not is_positive(value, required_type):
				self.lineedits[name].config(highlightthickness=2, highlightbackground='red')
				showerror("Некорректный ввод",
				          f"Поле {name} заполнено некорректно. ({name}=\"{value}\")\n\n"
				          f"Для справки: все поля должны содержать неотрицательные конечные вещественные числа, а последние 2 поля - только положительные целые числа")
				res = False
			else:
				self.lineedits[name].config(highlightthickness=0)
		return res


root = tk.Tk()
app = App(root)
root.mainloop()
