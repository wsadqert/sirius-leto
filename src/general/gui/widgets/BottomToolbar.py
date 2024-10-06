from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton, QWidget, QHBoxLayout

from src.general.gui.windows import BibliographyWindow, AboutWindow, TextTaskListWindow

tools = {
	"Задачник": TextTaskListWindow,
	"Список литературы": BibliographyWindow,
	"О программе": AboutWindow
}


class BottomToolbar(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.init_ui()

	def init_ui(self):
		self.setFixedHeight(50)
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)  # enable background changing feature
		self.setStyleSheet("border-radius: 25px; background-color: #d9d9d9;")

		self.layout = QHBoxLayout()
		tools_names = list(tools.keys())

		for tool_name in tools_names:
			item = QPushButton(tool_name, self)
			item.setStyleSheet("font-size: 20px; ")
			item.clicked.connect(self.generate_open_tool(tool_name))

			self.layout.addWidget(item)

		self.setLayout(self.layout)
		self.layout.addWidget(self)

	def generate_open_tool(self, tool_name):
		"""
		Wrapper for self.open_tool
		"""
		return lambda _: self.open_tool(tool_name)

	def open_tool(self, tool_name):
		print(tool_name)

		# if all pointers to `new_window` will expire, the object will be destroyed, which will cause window to close
		# therefore let's save the pointer to window to global variable
		global new_window  # noqa: undefined at module level

		new_window = tools[tool_name]()
		new_window.show()
