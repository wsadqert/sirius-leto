import tkinter as tk
import tkinter.font as tkFont
from rich.traceback import install
from ToolTip import CreateToolTip

install(show_locals=True, width=300)


def CustomLabel(text, font, align, place, size):
	label = tk.Label(root)

	match align:
		case 'left':
			anchor = 'w'
		case 'center':
			anchor = 'n'
		case 'right':
			anchor = 'e'
		case _:
			raise ValueError

	label["anchor"] = anchor
	label["font"] = font
	label["fg"] = "black"
	label["justify"] = align
	label["text"] = text
	label.place(x=place[0], y=place[1], width=size[0], height=size[1])


def CustomCheckBox(text, font, place, size, command, variable):
	CheckBox = tk.Checkbutton(root)

	CheckBox["anchor"] = "w"
	CheckBox["font"] = font
	CheckBox["fg"] = "black"
	CheckBox["justify"] = "left"
	CheckBox["text"] = text

	CheckBox["command"] = command
	CheckBox["variable"] = variable
	CheckBox["onvalue"] = True
	CheckBox["offvalue"] = False
	CheckBox.select()

	CheckBox.place(x=place[0], y=place[1], width=size[0], height=size[1])

	return CheckBox


def CustomRadiobutton(text, font, place, size, variable):
	RadioButton = tk.Radiobutton(root)
	RadioButton["anchor"] = "w"
	RadioButton["font"] = font
	RadioButton["fg"] = "black"
	RadioButton["justify"] = "left"
	RadioButton["text"] = text

	RadioButton["variable"] = variable
	RadioButton["value"] = text

	RadioButton.place(x=place[0], y=place[1], width=size[0], height=size[1])

	return RadioButton


def CustomLineEdit(font, align, place, size, variable):
	LineEdit = tk.Entry(root)

	LineEdit["borderwidth"] = "1px"
	LineEdit["font"] = font
	LineEdit["fg"] = "black"
	LineEdit["justify"] = align
	LineEdit["textvariable"] = variable

	LineEdit.place(x=place[0], y=place[1], width=size[0], height=size[1])

	return LineEdit


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

		font_10 = tkFont.Font(family='Times', size=10)
		font_18 = tkFont.Font(family='Times', size=18)
		font_33 = tkFont.Font(family='Times', size=33)

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
			"dt":               (120, 120),
			"t_max":            (120, 150),
			"l":                (380, 120),
			"alpha_start":      (380, 150),
			"k":                (380, 180),
			"m":                (380, 210),
			"render_dt":        (380, 290),
			"frames_count_fps": (380, 320),
		}
		self.__lineedits_size = (75, 25)
		self.__lineedits_variables = dict()

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
		self.radios = []
		self.__radio_variable = tk.StringVar(value="string")

		Label_title = CustomLabel(
			text="Настройки лаборатории",
			font=font_33,
			align="center",
			place=(0, 10),
			size=(527, 60)
		)

		for name, places in self.__labels_h2_info.items():  # create h2's
			Label_h2 = CustomLabel(
				text=name,
				font=font_18,
				align="left",
				place=places,
				size=self.__labels_h2_size
			)
		for name, places in self.__labels_info.items():  # create labels
			width = (120 if name == "frames_count_fps" else self.__labels_size[0])

			Label = CustomLabel(
				text=name + ' = ',
				font=font_10,
				align="right",
				place=places,
				size=(width,
				      self.__labels_size[1])
			)
		for name, places in self.__labels_units_info.items():  # create labels
			Label = CustomLabel(
				text=name,
				font=font_10,
				align="left",
				place=places,
				size=self.__labels_units_size,
			)
		for name, places in self.__radios_info.items():
			radio = CustomRadiobutton(text=name,
			                          font=font_10,
			                          place=places,
			                          size=self.__radios_size,
			                          variable=self.__radio_variable)
			self.radios.append(radio)
		for name, (text, place) in self.__checkboxes_info.items():
			current = tk.BooleanVar()

			if name == "windage":
				command = self.disable_windage_mode_selection
			else:
				command = lambda: None

			CustomCheckBox(
				text=text,
				font=font_10,
				place=place,
				command=command,
				variable=current,
				size=self.__checkboxes_size
			)

			self.__checkbox_variables[name] = current
		for name, places in self.__lineedits_info.items():
			current = tk.StringVar()

			LineEdit = CustomLineEdit(
				font=font_10,
				align="right",
				place=places,
				size=self.__lineedits_size,
				variable=current
			)

		self.GLabel_329 = tk.Label(root)
		self.GLabel_329["anchor"] = "w"
		self.GLabel_329["font"] = font_10
		self.GLabel_329["fg"] = "black"
		self.GLabel_329["justify"] = "left"
		self.GLabel_329["text"] = "Зависимость сопротивления\nвоздуха от скорости"
		self.GLabel_329.place(x=30, y=260, width=247, height=40)

		Button_start = tk.Button(root)
		Button_start["anchor"] = "center"
		Button_start["bg"] = "#00b800"
		Button_start["font"] = font_18
		Button_start["fg"] = "#ffffff"
		Button_start["justify"] = "center"
		Button_start["text"] = "Запуск!"
		Button_start["relief"] = "flat"
		Button_start.place(x=30, y=370, width=192, height=50)
		Button_start["command"] = self.GButton_912_command

	def disable_windage_mode_selection(self):
		variable = self.__checkbox_variables["windage"]

		if not variable.get():
			self.GLabel_329["fg"] = 'gray'
			for entry in self.radios:
				entry.configure(state='disabled')
		else:
			self.GLabel_329["fg"] = 'black'
			for entry in self.radios:
				entry.configure(state='normal')

	def GButton_912_command(self):
		print("command")
		root.destroy()


if __name__ == "__main__":
	root = tk.Tk()
	app = App(root)
	root.mainloop()
