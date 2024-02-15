from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
	QWidget,                    # the most general classes
	QDialog,                    # dialogs
	QHBoxLayout, QVBoxLayout,   # layouts
	QPlainTextEdit,             # text boxes
	QPushButton, QRadioButton,  # other interactive widgets
	QLabel
)
from src.general.gui.dialogs import TextDialog


class AboutDialog(TextDialog):
	def __init__(self):
		message = f"""
			<h1>О программе</h1><br/>
			lorem ipsum dolor sit amet, consectetur adipiscing
		"""

		super().__init__(message, "О программе")


class AboutEquipmentDialog(TextDialog):
	def __init__(self):
		message = f"""
			<h1>Об используемом оборудовании</h1><br/>
			lorem ipsum dolor sit amet, consectetur adipiscing
		"""

		super().__init__(message, "Об оборудовании")


class SuggestImprovementDialog(QDialog):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Предложить улучшения")
		self.init_ui()

	def init_ui(self):
		self.layout = QVBoxLayout()

		modes = QWidget()
		modes.setMaximumHeight(70)
		modes_layout = QHBoxLayout()

		rb_bug = QRadioButton("Сообщить о проблеме", modes)
		rb_bug.toggled.connect(lambda: input_field.setPlaceholderText("Подробно опишите проблему, с которой вы столкнулись"))  # noqa (ide error)

		rb_improvement = QRadioButton("Предложить улучшение", modes)
		rb_improvement.toggled.connect(lambda: input_field.setPlaceholderText("Подробно опишите улучшение, которое хотите предложить"))  # noqa (ide error)

		modes_layout.addWidget(rb_bug)
		modes_layout.addWidget(rb_improvement)
		modes.setLayout(modes_layout)

		text = QLabel("Ваше мнение очень важно для нас!")
		input_field = QPlainTextEdit()

		submit_button = QPushButton("Отправить")
		submit_button.clicked.connect(self.submit)  # noqa (ide error)

		rb_bug.setChecked(True)

		self.layout.addWidget(modes)
		self.layout.addWidget(text)
		self.layout.addWidget(input_field)
		self.layout.addWidget(submit_button)

		self.setLayout(self.layout)

	def submit(self):
		success_dialog = TextDialog("Ваше обращение отправлено. Спасибо, что помогаете сделать программу лучше!")
		success_dialog.exec()

		self.accept()  # close the dialog


class BottomToolbar(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.init_ui()

	def init_ui(self):
		self.setMaximumHeight(50)
		self.setMinimumHeight(50)
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
		self.setStyleSheet("border-radius: 25px; background-color: #d9d9d9;")

		self.layout = QHBoxLayout()
		tools_names = ["Файл", "Об оборудовании", "Предложить улучшения", "О программе"]

		for i, tool_name in enumerate(tools_names):
			item = QLabel(tool_name, self)
			item.setStyleSheet("font-size: 20px")
			item.setAlignment(Qt.AlignmentFlag.AlignCenter)
			item.mouseReleaseEvent = self.generate_open_tool(tool_name)

			self.layout.addWidget(item)

		self.setLayout(self.layout)
		self.layout.addWidget(self)

	def generate_open_tool(self, tool_name):
		def open_tool(self):
			if tool_name == "Файл":
				print(f"Opening tool {tool_name}")
				return

			new_dialog = {
				"Об оборудовании": AboutEquipmentDialog,
				"Предложить улучшения": SuggestImprovementDialog,
				"О программе": AboutDialog
			}[tool_name]()
			new_dialog.exec()

		return open_tool
