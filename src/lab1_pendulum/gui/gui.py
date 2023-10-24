import tkinter as tk
import tkinter.font as tkFont
from rich.traceback import install
from ToolTip import CreateToolTip

install(show_locals=True, width=300)


def CustomLabel(font, text, x, y, align):
	pass


def CustomCheckBox(font, text, x, y, command, variable):
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

	CheckBox.place(x=x, y=y, width=230, height=30)

	return CheckBox


def CustomRadiobutton(font, text: str, x, y, variable):
	RadioButton = tk.Radiobutton(root)
	RadioButton["anchor"] = "w"
	RadioButton["font"] = font
	RadioButton["fg"] = "black"
	RadioButton["justify"] = "left"
	RadioButton["text"] = text

	RadioButton["variable"] = variable
	RadioButton["value"] = text

	RadioButton.place(x=x, y=y, width=100, height=25)

	return RadioButton


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
		self.__labels_h2_width = 200
		self.__labels_h2_height = 35

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
		self.__labels_width = 100
		self.__labels_height = 25

		self.__labels_units_info = {
			"с ": (200, 120),
			"с": (200, 150),
			"м": (460, 120),
			"рад": (460, 150),
			"кг/с": (460, 180),
			"кг": (460, 210),
		}
		self.__labels_units_width = 30
		self.__labels_units_height = 25

		self.__checkboxes_info = {
			"theory": ("Расчитывать аналитическое решение", (40, 190)),
			"windage": ("Учитывать сопротивление воздуха", (40, 220)),
			"extremums": ("Отображать пики на графике", (280, 350)),
		}
		self.__checkbox_variables = dict()

		self.radios = []
		self.__radios_info = {
			"kv": (40, 300),
			"kv^2": (130, 300),
			"реалистично": (40, 320)
		}
		self.__radio_variable = tk.StringVar(value="string")

		Label_title = tk.Label(root)
		Label_title["anchor"] = "center"
		Label_title["font"] = font_33
		Label_title["fg"] = "black"
		Label_title["justify"] = "center"
		Label_title["text"] = "Настройки лаборатории"
		Label_title.place(x=0, y=20, width=527, height=50)

		for name in self.__labels_h2_info.keys():  # create h2's
			places = self.__labels_h2_info[name]

			Label_h2 = tk.Label(root)
			Label_h2["font"] = font_18
			Label_h2["fg"] = "black"
			Label_h2["justify"] = "left"
			Label_h2["text"] = name
			Label_h2.place(x=places[0],
			               y=places[1],
			               width=self.__labels_h2_width,
			               height=self.__labels_h2_height)
		for name in self.__labels_info.keys():  # create labels
			place = self.__labels_info[name]

			Label = tk.Label(root)
			Label["anchor"] = "e"
			Label["font"] = font_10
			Label["fg"] = "black"
			Label["justify"] = "right"
			Label["text"] = name + ' = '

			Label.place(x=place[0],
			            y=place[1],
			            width=120 if name == "frames_count_fps" else self.__labels_width,
			            height=self.__labels_height)
		for name in self.__labels_units_info.keys():  # create labels
			place = self.__labels_units_info[name]

			Label = tk.Label(root)
			Label["anchor"] = "w"
			Label["font"] = font_10
			Label["fg"] = "black"
			Label["justify"] = "left"
			Label["text"] = name

			Label.place(x=place[0],
			            y=place[1],
			            width=self.__labels_units_width,
			            height=self.__labels_units_height)
		for name in self.__radios_info.keys():
			place = self.__radios_info[name]

			radio = CustomRadiobutton(font=font_10,
			                          text=name,
			                          x=place[0],
			                          y=place[1],
			                          variable=self.__radio_variable)

			self.radios.append(radio)
		for name in self.__checkboxes_info.keys():
			current = tk.BooleanVar()

			if name == "windage":
				command = self.disable_windage_mode_selection
			else:
				command = lambda x: None

			CustomCheckBox(font=font_10,
			               text=self.__checkboxes_info[name][0],
			               x=self.__checkboxes_info[name][1][0],
			               y=self.__checkboxes_info[name][1][1],
			               command=command,
			               variable=current)

			self.__checkbox_variables[name] = current

		self.GLabel_329 = tk.Label(root)
		self.GLabel_329["anchor"] = "w"
		self.GLabel_329["font"] = font_10
		self.GLabel_329["fg"] = "black"
		self.GLabel_329["justify"] = "left"
		self.GLabel_329["text"] = "Зависимость сопротивления\nвоздуха от скорости"
		self.GLabel_329.place(x=30, y=260, width=247, height=40)

		GLineEdit_611 = tk.Entry(root)
		GLineEdit_611["borderwidth"] = "1px"
		GLineEdit_611["font"] = font_10
		GLineEdit_611["fg"] = "black"
		GLineEdit_611["justify"] = "right"
		GLineEdit_611["text"] = "alpha_start"
		GLineEdit_611.place(x=380, y=150, width=70, height=25)

		GLineEdit_837 = tk.Entry(root)
		GLineEdit_837["borderwidth"] = "1px"
		GLineEdit_837["font"] = font_10
		GLineEdit_837["fg"] = "black"
		GLineEdit_837["justify"] = "right"
		GLineEdit_837["text"] = "k"
		GLineEdit_837.place(x=380, y=180, width=70, height=25)

		GLineEdit_129 = tk.Entry(root)
		GLineEdit_129["borderwidth"] = "1px"
		GLineEdit_129["font"] = font_10
		GLineEdit_129["fg"] = "black"
		GLineEdit_129["justify"] = "right"
		GLineEdit_129["text"] = "m"
		GLineEdit_129.place(x=380, y=210, width=70, height=25)

		GLineEdit_593 = tk.Entry(root)
		GLineEdit_593["borderwidth"] = "1px"
		GLineEdit_593["font"] = font_10
		GLineEdit_593["fg"] = "black"
		GLineEdit_593["justify"] = "right"
		GLineEdit_593["text"] = "render_dt"
		GLineEdit_593.place(x=380, y=290, width=70, height=25)

		GLineEdit_126 = tk.Entry(root)
		GLineEdit_126["borderwidth"] = "1px"
		GLineEdit_126["font"] = font_10
		GLineEdit_126["fg"] = "black"
		GLineEdit_126["justify"] = "right"
		GLineEdit_126["text"] = "frames_count_fps"
		GLineEdit_126.place(x=380, y=320, width=70, height=25)

		GLineEdit_323 = tk.Entry(root)
		GLineEdit_323["borderwidth"] = "1px"
		GLineEdit_323["font"] = font_10
		GLineEdit_323["fg"] = "black"
		GLineEdit_323["justify"] = "right"
		GLineEdit_323["text"] = "dt"
		GLineEdit_323.place(x=120, y=120, width=70, height=25)

		GLineEdit_140 = tk.Entry(root)
		GLineEdit_140["borderwidth"] = "1px"
		GLineEdit_140["font"] = font_10
		GLineEdit_140["fg"] = "black"
		GLineEdit_140["justify"] = "right"
		GLineEdit_140["text"] = "t_max"
		GLineEdit_140.place(x=120, y=150, width=70, height=25)

		GLineEdit_715 = tk.Entry(root)
		GLineEdit_715["borderwidth"] = "1px"
		GLineEdit_715["font"] = font_10
		GLineEdit_715["fg"] = "black"
		GLineEdit_715["justify"] = "right"
		GLineEdit_715["text"] = "l"
		GLineEdit_715.place(x=380, y=120, width=70, height=25)

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
