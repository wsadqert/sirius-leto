import tkinter as tk

__all__ = ["CustomLabel", "CustomRadioButton", "CustomLineEdit", "CustomCheckBox"]

# in constructors, I can use `super().__init__(**kwargs)`, but we must be able to override default settings,
# therefore I use `for ... in kwargs.items()` expression


class CustomLabel(tk.Label):
	def __init__(self, text, font, align, place, size, **kwargs):
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

		for key, val in kwargs.items():
			self[key] = val

		self.place(x=place[0], y=place[1], width=size[0], height=size[1])


class CustomCheckBox(tk.Checkbutton):
	def __init__(self, text, font, place, size, command, variable, select=True, **kwargs):
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

		for key, val in kwargs.items():
			self[key] = val

		if select:
			self.select()

		self.place(x=place[0], y=place[1], width=size[0], height=size[1])


class CustomRadioButton(tk.Radiobutton):
	def __init__(self, text, font, place, size, variable, value, command: () = lambda: None, **kwargs):
		super().__init__()

		self["anchor"] = "w"
		self["font"] = font
		self["fg"] = "black"
		self["justify"] = "left"
		self["text"] = text

		self["variable"] = variable
		self["value"] = value
		self["command"] = command

		for key, val in kwargs.items():
			self[key] = val

		self.place(x=place[0], y=place[1], width=size[0], height=size[1])


class CustomLineEdit(tk.Entry):
	def __init__(self, font, align, place, size, variable, default_value: str = "", **kwargs):
		super().__init__()

		self["borderwidth"] = "1px"
		self["font"] = font
		self["fg"] = "black"
		self["justify"] = align
		self["textvariable"] = variable

		for key, val in kwargs.items():
			self[key] = val

		self.insert(0, default_value)

		self.place(x=place[0], y=place[1], width=size[0], height=size[1])

