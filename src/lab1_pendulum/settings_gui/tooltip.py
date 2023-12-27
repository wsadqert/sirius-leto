# https://stackoverflow.com/a/56749167

import tkinter as tk

__all__ = ["create_tooltip"]


class ToolTip(object):
	def __init__(self, widget: tk.Widget):
		self.widget = widget
		self.tipwindow = None
		self.id = None
		self.x = self.y = 0

	def showtip(self, text: str):
		"""Display text in tooltip window"""
		self.text = text
		if self.tipwindow or not self.text:
			return
		x, y, cx, cy = self.widget.bbox("insert")
		x = x + self.widget.winfo_rootx() + 57
		y = y + cy + self.widget.winfo_rooty() + 27
		self.tipwindow = tw = tk.Toplevel(self.widget)
		tw.wm_overrideredirect(True)
		tw.wm_geometry("+%d+%d" % (x, y))
		label = tk.Label(tw, text=self.text, justify=tk.LEFT,
		                 background="#ffffe0", relief=tk.SOLID, borderwidth=1,
		                 font=("tahoma", "8", "normal"))
		label.pack(ipadx=1)

	def hidetip(self):
		tw = self.tipwindow
		self.tipwindow = None
		if tw:
			tw.destroy()


def create_tooltip(widget, text):
	tooltip = ToolTip(widget)

	def enter(event):
		tooltip.showtip(text)

	def leave(event):
		tooltip.hidetip()

	widget.bind('<Enter>', enter)
	widget.bind('<Leave>', leave)
