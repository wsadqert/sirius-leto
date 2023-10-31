import tkinter as tk

__all__ = ["CustomLabel", "CustomRadiobutton", "CustomLineEdit", "CustomCheckBox"]


def CustomLabel(root, text, font, align, place, size):
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

	return label


def CustomCheckBox(root, text, font, place, size, command, variable):
	checkbox = tk.Checkbutton(root)

	checkbox["anchor"] = "w"
	checkbox["font"] = font
	checkbox["fg"] = "black"
	checkbox["justify"] = "left"
	checkbox["text"] = text

	checkbox["command"] = command
	checkbox["variable"] = variable
	checkbox["onvalue"] = True
	checkbox["offvalue"] = False
	checkbox.select()

	checkbox.place(x=place[0], y=place[1], width=size[0], height=size[1])

	return checkbox


def CustomRadiobutton(root, text, font, place, size, variable, value):
	radiobutton = tk.Radiobutton(root)
	radiobutton["anchor"] = "w"
	radiobutton["font"] = font
	radiobutton["fg"] = "black"
	radiobutton["justify"] = "left"
	radiobutton["text"] = text

	radiobutton["variable"] = variable
	radiobutton["value"] = value

	radiobutton.place(x=place[0], y=place[1], width=size[0], height=size[1])

	return radiobutton


def CustomLineEdit(root, font, align, place, size, variable, default_value: str = ''):
	lineedit = tk.Entry(root)

	lineedit["borderwidth"] = "1px"
	lineedit["font"] = font
	lineedit["fg"] = "black"
	lineedit["justify"] = align
	lineedit["textvariable"] = variable

	lineedit.insert(0, default_value)

	lineedit.place(x=place[0], y=place[1], width=size[0], height=size[1])

	return lineedit
