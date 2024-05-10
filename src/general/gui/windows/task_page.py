import os.path
from typing import Callable

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
	QWidget,                                # the most general classes
	QDialogButtonBox,                       # dialogs
	QVBoxLayout, QHBoxLayout, QFormLayout,  # layouts
	QTextBrowser, QLineEdit,                # text boxes
	QPushButton,                            # other interactive widgets
	QLabel
)
import json

from src.general.constants import ASSETS_ROOT
from src.general.gui.dialogs import TextDialog
from src.general.checks import is_positive

__all__ = ["TaskPage"]

labs = json.load(open(os.path.join(ASSETS_ROOT, "labs_description.json"), encoding='utf-8'))
QAlignment = Qt.AlignmentFlag


class IncorrectInputDialog(TextDialog):
	def __init__(self, fields: list[str]):
		if len(fields) == 1:
			message = f"Field <span style='color: red'>{fields[0]}</span> is filled incorrectly"
		else:
			message = f"Fields <span style='color: red'>{'</span>, <span style=\'color: red\'>'.join(fields)}</span> are filled incorrectly"

		super().__init__(
			text=message,
			title="Некорректный ввод",
			buttons=QDialogButtonBox.StandardButton.Ok
		)


class TaskPage(QWidget):
	def __init__(self, task_number: tuple[int, int], back_function: Callable):
		super().__init__()

		self.grade_number, self.task_number = task_number
		self.back_function = back_function
		self.description = labs[str(self.grade_number)][self.task_number - 1]

		self.title = self.description["title"]
		self.target = self.description["target"]
		self.hardware = self.description["hardware"]
		self.progress = self.description["progress"]
		self.target_names = self.description["target_names"]
		self.units = self.description["units"]
		self.correct_answers = self.description["correct_answers"]

		self.task_text = fr"""
			<h2 align="center">Условие задачи</h2>
			
			<h3>Цель</h3>
			<p>{self.target}</p>
			<br/>
			
			<h3>Оборудование</h3>
			{self.hardware}
			<h3>Ход работы</h3>
			
			<ol>
				{'\n'.join([f"<li>{i}</li>" for i in self.progress])}
			</ol>
		"""

		self.resize(1200, 800)
		self.setWindowTitle("Лаборатория")

		self.init_ui()

	def init_ui(self):
		layout = QVBoxLayout()

		title_layout = QHBoxLayout()

		back_button = QPushButton()
		back_button.setIcon(QIcon(os.path.join(ASSETS_ROOT, "icons", "arrow_left_in_circle", "arrow_left_in_circle_black_451px.png")))
		back_button.setIconSize(QSize(50, 50))
		back_button.setMaximumWidth(50)
		back_button.clicked.connect(lambda _e: self.back_function(self.grade_number)())
		back_button.setStyleSheet("background-color: transparent; ")

		title_label = QLabel(self.title)
		title_label.setStyleSheet("font-size: 30px")
		title_label.setAlignment(QAlignment.AlignCenter)

		columns = QWidget()
		columns_layout = QHBoxLayout()

		left_text = QTextBrowser(columns)
		left_text.setHtml(self.task_text)

		form = QWidget(columns)
		form_layout = QFormLayout()
		form.setLayout(form_layout)

		self.inputs: dict[str, QLineEdit] = {}

		# Add input fields to the form
		for name, unit in zip(self.target_names, self.units):
			input1 = QLineEdit()
			input1.setPlaceholderText(unit)
			form_layout.addRow(name, input1)

			self.inputs[name] = input1

		submit_button = QPushButton('Отправить', columns)
		form_layout.addRow(submit_button)

		title_layout.addWidget(back_button)
		title_layout.addWidget(title_label)
		title_widget = QWidget()
		title_widget.setLayout(title_layout)

		columns_layout.addWidget(left_text)
		columns_layout.addWidget(form)
		columns.setLayout(columns_layout)

		submit_button.clicked.connect(self.submit_form)  # noqa (ide error)

		layout.addWidget(title_widget)
		layout.addWidget(columns)

		self.setLayout(layout)

	def keyPressEvent(self, e):
		if e.key() == Qt.Key.Key_Return:
			self.submit_form()

	def change_border(self, name, state):
		if state:
			border_style = "none"
		else:
			border_style = "2px solid red"
		self.inputs[name].setStyleSheet(f"border: {border_style}")

	def check_correctness(self):
		incorrect_names = []

		for name, val in self.inputs.items():
			is_correct = is_positive(val.text())
			self.change_border(name, is_correct)

			if not is_correct:
				incorrect_names.append(name)

		if incorrect_names:
			IncorrectInputDialog(incorrect_names).show()

		return not len(incorrect_names)

	def check_answers(self):
		# assuming all input fields are filled correctly

		for name, val in self.inputs.items():
			pass

	def submit_form(self):
		if not self.check_correctness():
			return

		print('Form submitted:')

		for name, val in self.inputs.items():
			print(f"{name}: {val.text()}")
