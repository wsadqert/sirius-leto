import tkinter as tk

__all__ = ["CustomLabel", "CustomRadioButton", "CustomLineEdit", "CustomCheckBox"]


class CustomLabel(tk.Label):
	def __init__(self, text, font, align, place, size):
		super().__init__()

		match align:
			case 'left':
				anchor = 'w'
			case 'center':
				anchor = 'n'
			case 'right':
				anchor = 'e'
			case _:
				raise ValueError

		self["anchor"] = anchor
		self["font"] = font
		self["fg"] = "black"
		self["justify"] = align
		self["text"] = text
		self.place(x=place[0], y=place[1], width=size[0], height=size[1])


class CustomCheckBox(tk.Checkbutton):
	def __init__(self, text, font, place, size, command, variable, select=True):
		super().__init__()
		self["anchor"] = "w"
		self["font"] = font
		self["fg"] = "black"
		self["justify"] = "left"
		self["text"] = text

		self["command"] = command
		self["variable"] = variable
		self["onvalue"] = True
		self["offvalue"] = False

		if select:
			self.select()

		self.place(x=place[0], y=place[1], width=size[0], height=size[1])


class CustomRadioButton(tk.Radiobutton):
	def __init__(self, text, font, place, size, variable, value, command: () = lambda: None):
		super().__init__()
		self["anchor"] = "w"
		self["font"] = font
		self["fg"] = "black"
		self["justify"] = "left"
		self["text"] = text

		self["variable"] = variable
		self["value"] = value
		self["command"] = command

		self.place(x=place[0], y=place[1], width=size[0], height=size[1])


class CustomLineEdit(tk.Entry):
	def __init__(self, font, align, place, size, variable, default_value: str = ""):
		super().__init__()

		self["borderwidth"] = "1px"
		self["font"] = font
		self["fg"] = "black"
		self["justify"] = align
		self["textvariable"] = variable

		self.insert(0, default_value)

		self.place(x=place[0], y=place[1], width=size[0], height=size[1])

