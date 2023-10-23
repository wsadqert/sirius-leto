import tkinter as tk
import tkinter.font as tkFont


class App:
	def __init__(self, root):
		# setting title
		root.title("Settings")
		# setting window size
		width = 527
		height = 446
		screenwidth = root.winfo_screenwidth()
		screenheight = root.winfo_screenheight()
		alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
		root.geometry(alignstr)
		root.resizable(width=False, height=False)

		GLabel_471 = tk.Label(root)
		GLabel_471["anchor"] = "center"
		ft = tkFont.Font(family='Times', size=33)
		GLabel_471["font"] = ft
		GLabel_471["fg"] = "#333333"
		GLabel_471["justify"] = "center"
		GLabel_471["text"] = "Настройки лаборатрии"
		GLabel_471.place(x=0, y=20, width=527, height=50)

		GCheckBox_688 = tk.Checkbutton(root)
		GCheckBox_688["anchor"] = "w"
		ft = tkFont.Font(family='Times', size=10)
		GCheckBox_688["font"] = ft
		GCheckBox_688["fg"] = "#333333"
		GCheckBox_688["justify"] = "left"
		GCheckBox_688["text"] = "Учитывать сопротивление воздуха"
		GCheckBox_688.place(x=40, y=220, width=226, height=30)
		GCheckBox_688["offvalue"] = "0"
		GCheckBox_688["onvalue"] = "1"
		GCheckBox_688["command"] = self.GCheckBox_688_command

		GCheckBox_599 = tk.Checkbutton(root)
		GCheckBox_599["anchor"] = "w"
		ft = tkFont.Font(family='Times', size=10)
		GCheckBox_599["font"] = ft
		GCheckBox_599["fg"] = "#333333"
		GCheckBox_599["justify"] = "left"
		GCheckBox_599["text"] = "Расчитывать аналитическое решение"
		GCheckBox_599.place(x=40, y=190, width=227, height=30)
		GCheckBox_599["offvalue"] = "0"
		GCheckBox_599["onvalue"] = "1"
		GCheckBox_599["command"] = self.GCheckBox_599_command

		GCheckBox_893 = tk.Checkbutton(root)
		GCheckBox_893["anchor"] = "e"
		ft = tkFont.Font(family='Times', size=10)
		GCheckBox_893["font"] = ft
		GCheckBox_893["fg"] = "#333333"
		GCheckBox_893["justify"] = "left"
		GCheckBox_893["text"] = "Отображать пики на графике"
		GCheckBox_893.place(x=280, y=350, width=189, height=35)
		GCheckBox_893["offvalue"] = "0"
		GCheckBox_893["onvalue"] = "1"
		GCheckBox_893["command"] = self.GCheckBox_893_command

		GLabel_603 = tk.Label(root)
		GLabel_603["anchor"] = "e"
		ft = tkFont.Font(family='Times', size=10)
		GLabel_603["font"] = ft
		GLabel_603["fg"] = "#333333"
		GLabel_603["justify"] = "right"
		GLabel_603["text"] = "dt"
		GLabel_603.place(x=40, y=120, width=70, height=25)

		GLabel_77 = tk.Label(root)
		GLabel_77["anchor"] = "e"
		ft = tkFont.Font(family='Times', size=10)
		GLabel_77["font"] = ft
		GLabel_77["fg"] = "#333333"
		GLabel_77["justify"] = "right"
		GLabel_77["text"] = "t_max"
		GLabel_77.place(x=40, y=150, width=70, height=25)

		GLabel_92 = tk.Label(root)
		GLabel_92["anchor"] = "e"
		ft = tkFont.Font(family='Times', size=10)
		GLabel_92["font"] = ft
		GLabel_92["fg"] = "#333333"
		GLabel_92["justify"] = "right"
		GLabel_92["text"] = "l"
		GLabel_92.place(x=290, y=120, width=70, height=25)

		GLineEdit_715 = tk.Entry(root)
		GLineEdit_715["borderwidth"] = "1px"
		ft = tkFont.Font(family='Times', size=10)
		GLineEdit_715["font"] = ft
		GLineEdit_715["fg"] = "#333333"
		GLineEdit_715["justify"] = "right"
		GLineEdit_715["text"] = "l"
		GLineEdit_715.place(x=380, y=120, width=70, height=25)

		GLabel_210 = tk.Label(root)
		GLabel_210["anchor"] = "e"
		ft = tkFont.Font(family='Times', size=10)
		GLabel_210["font"] = ft
		GLabel_210["fg"] = "#333333"
		GLabel_210["justify"] = "right"
		GLabel_210["text"] = "alpha_start"
		GLabel_210.place(x=290, y=150, width=70, height=25)

		GLineEdit_611 = tk.Entry(root)
		GLineEdit_611["borderwidth"] = "1px"
		ft = tkFont.Font(family='Times', size=10)
		GLineEdit_611["font"] = ft
		GLineEdit_611["fg"] = "#333333"
		GLineEdit_611["justify"] = "right"
		GLineEdit_611["text"] = "alpha_start"
		GLineEdit_611.place(x=380, y=150, width=70, height=25)

		GLabel_939 = tk.Label(root)
		GLabel_939["anchor"] = "e"
		ft = tkFont.Font(family='Times', size=10)
		GLabel_939["font"] = ft
		GLabel_939["fg"] = "#333333"
		GLabel_939["justify"] = "right"
		GLabel_939["text"] = "k"
		GLabel_939.place(x=290, y=180, width=70, height=25)

		GLineEdit_837 = tk.Entry(root)
		GLineEdit_837["borderwidth"] = "1px"
		ft = tkFont.Font(family='Times', size=10)
		GLineEdit_837["font"] = ft
		GLineEdit_837["fg"] = "#333333"
		GLineEdit_837["justify"] = "right"
		GLineEdit_837["text"] = "k"
		GLineEdit_837.place(x=380, y=180, width=70, height=25)

		GLabel_484 = tk.Label(root)
		GLabel_484["anchor"] = "e"
		ft = tkFont.Font(family='Times', size=10)
		GLabel_484["font"] = ft
		GLabel_484["fg"] = "#333333"
		GLabel_484["justify"] = "right"
		GLabel_484["text"] = "m"
		GLabel_484.place(x=290, y=210, width=70, height=25)

		GLineEdit_129 = tk.Entry(root)
		GLineEdit_129["borderwidth"] = "1px"
		ft = tkFont.Font(family='Times', size=10)
		GLineEdit_129["font"] = ft
		GLineEdit_129["fg"] = "#333333"
		GLineEdit_129["justify"] = "right"
		GLineEdit_129["text"] = "m"
		GLineEdit_129.place(x=380, y=210, width=70, height=25)

		GLabel_664 = tk.Label(root)
		GLabel_664["anchor"] = "e"
		ft = tkFont.Font(family='Times', size=10)
		GLabel_664["font"] = ft
		GLabel_664["fg"] = "#333333"
		GLabel_664["justify"] = "right"
		GLabel_664["text"] = "frames_count_fps"
		GLabel_664.place(x=250, y=320, width=115, height=30)

		GLineEdit_593 = tk.Entry(root)
		GLineEdit_593["borderwidth"] = "1px"
		ft = tkFont.Font(family='Times', size=10)
		GLineEdit_593["font"] = ft
		GLineEdit_593["fg"] = "#333333"
		GLineEdit_593["justify"] = "right"
		GLineEdit_593["text"] = "render_dt"
		GLineEdit_593.place(x=380, y=290, width=70, height=25)

		GLabel_759 = tk.Label(root)
		ft = tkFont.Font(family='Times', size=18)
		GLabel_759["font"] = ft
		GLabel_759["fg"] = "#333333"
		GLabel_759["justify"] = "left"
		GLabel_759["text"] = "Физика"
		GLabel_759.place(x=290, y=80, width=177, height=39)

		GLabel_653 = tk.Label(root)
		GLabel_653["anchor"] = "e"
		ft = tkFont.Font(family='Times', size=10)
		GLabel_653["font"] = ft
		GLabel_653["fg"] = "#333333"
		GLabel_653["justify"] = "right"
		GLabel_653["text"] = "render_dt"
		GLabel_653.place(x=290, y=290, width=70, height=25)

		GLabel_236 = tk.Label(root)
		ft = tkFont.Font(family='Times', size=18)
		GLabel_236["font"] = ft
		GLabel_236["fg"] = "#333333"
		GLabel_236["justify"] = "left"
		GLabel_236["text"] = "Рендер"
		GLabel_236.place(x=290, y=250, width=180, height=33)

		GLineEdit_126 = tk.Entry(root)
		GLineEdit_126["borderwidth"] = "1px"
		ft = tkFont.Font(family='Times', size=10)
		GLineEdit_126["font"] = ft
		GLineEdit_126["fg"] = "#333333"
		GLineEdit_126["justify"] = "right"
		GLineEdit_126["text"] = "frames_count_fps"
		GLineEdit_126.place(x=380, y=320, width=70, height=25)

		GButton_912 = tk.Button(root)
		GButton_912["anchor"] = "center"
		GButton_912["bg"] = "#00b800"
		ft = tkFont.Font(family='Times', size=18)
		GButton_912["font"] = ft
		GButton_912["fg"] = "#ffffff"
		GButton_912["justify"] = "center"
		GButton_912["text"] = "Запуск!"
		GButton_912["relief"] = "flat"
		GButton_912.place(x=30, y=370, width=192, height=50)
		GButton_912["command"] = self.GButton_912_command

		GLineEdit_323 = tk.Entry(root)
		GLineEdit_323["borderwidth"] = "1px"
		ft = tkFont.Font(family='Times', size=10)
		GLineEdit_323["font"] = ft
		GLineEdit_323["fg"] = "#333333"
		GLineEdit_323["justify"] = "right"
		GLineEdit_323["text"] = "dt"
		GLineEdit_323.place(x=120, y=120, width=70, height=25)

		GLineEdit_140 = tk.Entry(root)
		GLineEdit_140["borderwidth"] = "1px"
		ft = tkFont.Font(family='Times', size=10)
		GLineEdit_140["font"] = ft
		GLineEdit_140["fg"] = "#333333"
		GLineEdit_140["justify"] = "right"
		GLineEdit_140["text"] = "t_max"
		GLineEdit_140.place(x=120, y=150, width=70, height=25)

		GLabel_844 = tk.Label(root)
		GLabel_844["anchor"] = "w"
		ft = tkFont.Font(family='Times', size=10)
		GLabel_844["font"] = ft
		GLabel_844["fg"] = "#333333"
		GLabel_844["justify"] = "left"
		GLabel_844["text"] = "с"
		GLabel_844.place(x=200, y=120, width=70, height=25)

		GLabel_363 = tk.Label(root)
		GLabel_363["anchor"] = "w"
		ft = tkFont.Font(family='Times', size=10)
		GLabel_363["font"] = ft
		GLabel_363["fg"] = "#333333"
		GLabel_363["justify"] = "left"
		GLabel_363["text"] = "с"
		GLabel_363.place(x=200, y=150, width=70, height=25)

		GLabel_675 = tk.Label(root)
		GLabel_675["anchor"] = "w"
		ft = tkFont.Font(family='Times', size=10)
		GLabel_675["font"] = ft
		GLabel_675["fg"] = "#333333"
		GLabel_675["justify"] = "left"
		GLabel_675["text"] = "м"
		GLabel_675.place(x=460, y=120, width=70, height=25)

		GLabel_874 = tk.Label(root)
		GLabel_874["anchor"] = "w"
		ft = tkFont.Font(family='Times', size=10)
		GLabel_874["font"] = ft
		GLabel_874["fg"] = "#333333"
		GLabel_874["justify"] = "left"
		GLabel_874["text"] = "рад"
		GLabel_874.place(x=460, y=150, width=70, height=25)

		GLabel_678 = tk.Label(root)
		GLabel_678["anchor"] = "w"
		ft = tkFont.Font(family='Times', size=10)
		GLabel_678["font"] = ft
		GLabel_678["fg"] = "#333333"
		GLabel_678["justify"] = "left"
		GLabel_678["text"] = "кг/с"
		GLabel_678.place(x=460, y=180, width=70, height=25)

		GLabel_94 = tk.Label(root)
		GLabel_94["anchor"] = "w"
		ft = tkFont.Font(family='Times', size=10)
		GLabel_94["font"] = ft
		GLabel_94["fg"] = "#333333"
		GLabel_94["justify"] = "left"
		GLabel_94["text"] = "кг"
		GLabel_94.place(x=460, y=210, width=70, height=25)

		GLabel_126 = tk.Label(root)
		ft = tkFont.Font(family='Times', size=18)
		GLabel_126["font"] = ft
		GLabel_126["fg"] = "#333333"
		GLabel_126["justify"] = "center"
		GLabel_126["text"] = "Настройки модели"
		GLabel_126.place(x=40, y=80, width=210, height=37)

		GRadio_802 = tk.Radiobutton(root)
		GRadio_802["anchor"] = "w"
		ft = tkFont.Font(family='Times', size=10)
		GRadio_802["font"] = ft
		GRadio_802["fg"] = "#333333"
		GRadio_802["justify"] = "left"
		GRadio_802["text"] = "kv"
		GRadio_802.place(x=40, y=300, width=85, height=25)
		GRadio_802["value"] = "windage_mode"
		GRadio_802["command"] = self.GRadio_802_command

		GLabel_329 = tk.Label(root)
		GLabel_329["anchor"] = "w"
		ft = tkFont.Font(family='Times', size=10)
		GLabel_329["font"] = ft
		GLabel_329["fg"] = "#333333"
		GLabel_329["justify"] = "left"
		GLabel_329["text"] = "Зависимость сопротивления \n воздуха от скорости"
		GLabel_329.place(x=30, y=260, width=247, height=40)

		GRadio_259 = tk.Radiobutton(root)
		GRadio_259["anchor"] = "w"
		ft = tkFont.Font(family='Times', size=10)
		GRadio_259["font"] = ft
		GRadio_259["fg"] = "#333333"
		GRadio_259["justify"] = "left"
		GRadio_259["text"] = "kv^2"
		GRadio_259.place(x=130, y=300, width=85, height=25)
		GRadio_259["value"] = "windage_mode"
		GRadio_259["command"] = self.GRadio_259_command

		GRadio_690 = tk.Radiobutton(root)
		GRadio_690["anchor"] = "w"
		ft = tkFont.Font(family='Times', size=10)
		GRadio_690["font"] = ft
		GRadio_690["fg"] = "#333333"
		GRadio_690["justify"] = "left"
		GRadio_690["text"] = "реалистичное сопротивление"
		GRadio_690.place(x=40, y=320, width=209, height=34)
		GRadio_690["command"] = self.GRadio_690_command

	def GCheckBox_688_command(self):
		print("command")

	def GCheckBox_599_command(self):
		print("command")

	def GCheckBox_893_command(self):
		print("command")

	def GButton_912_command(self):
		print("command")

	def GRadio_802_command(self):
		print("command")

	def GRadio_259_command(self):
		print("command")

	def GRadio_690_command(self):
		print("command")


if __name__ == "__main__":
	root = tk.Tk()
	app = App(root)
	root.mainloop()
