import logging
from typing import Callable
import json

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel

from src.general.gui.key_handler import _handle_key_gen
from src.general.gui.widgets.BottomToolbar import BottomToolbar
from src.general.constants import *

__all__ = ["GradePage"]

labs = json.load(open(f"{ASSETS_ROOT}\\labs_description.json", encoding="utf-8"))


class GradePage(QWidget):
	def __init__(self, grade_number: int, back_function: Callable, open_task_function: Callable):
		super().__init__()
		self.grade_number = grade_number
		self.back_function = back_function
		self.open_task_function = open_task_function

		self.init_ui()

	def init_ui(self):
		self.setObjectName("grade_window")  # for using custom CSS selector

		self.setWindowTitle(f"{self.grade_number} класс")
		self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
		self.setStyleSheet("""
			QWidget#grade_window {
			    background-image: url("assets/images/background/grade_window.jpg");
			    background-repeat: no-repeat;
		    }
		""")
		self.keyPressEvent = _handle_key_gen(Qt.Key.Key_Backspace, self.back_function)

		title_layout = QHBoxLayout()

		back_button = QPushButton()
		back_button.setIcon(QIcon(f"{ICONS_ROOT}\\arrow_left_in_circle\\arrow_left_in_circle_white_451px.png"))
		back_button.setIconSize(QSize(50, 50))
		back_button.setFixedWidth(50)
		back_button.clicked.connect(self.back_function)  # noqa (ide error)
		back_button.setStyleSheet("background-color: transparent; ")

		# title
		title_label = QLabel(f"{self.grade_number} класс")
		title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
		title_label.setStyleSheet("color: white; font-size: 30px; ")

		# subtitle
		subtitle_label = QLabel("Виртуальные лабораторные работы по физике")
		subtitle_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
		subtitle_label.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 20px; ")

		labs_layout = QVBoxLayout()

		for i, lab in enumerate(labs[str(self.grade_number)]):
			lab_name = lab["title"]

			lab_name_widget = QLabel(f"{i+1}. {lab_name}")
			lab_name_widget.setStyleSheet("font-size: 25px; color: #00ff00")
			lab_name_widget.setAlignment(Qt.AlignmentFlag.AlignLeft)
			lab_name_widget.setMaximumHeight(40)
			lab_name_widget.mouseReleaseEvent = self.generate_open_task(i+1)
			labs_layout.addWidget(lab_name_widget)

		# toolbar
		toolbar = BottomToolbar()

		# layout of window
		title_layout.addWidget(back_button)
		title_layout.addSpacing(10)
		title_layout.addWidget(title_label)
		title_layout.addWidget(subtitle_label)

		title_widget = QWidget()
		title_widget.setLayout(title_layout)
		title_widget.setMaximumHeight(70)

		labs_widget = QWidget()
		labs_widget.setLayout(labs_layout)

		layout = QVBoxLayout()
		layout.addWidget(title_widget)
		layout.addWidget(labs_widget)
		layout.addWidget(toolbar)

		self.setLayout(layout)
		layout.addWidget(self)

	def open_task(self, task_number: int):
		print('open task', task_number)

		if (self.grade_number, task_number) == (9, 3):
			from src.lab1_pendulum import start
			try:
				start()
			except Exception as e:
				logging.exception(e)
				raise

		self.open_task_function((self.grade_number, task_number))

	def generate_open_task(self, task_number: int):
		return lambda task: self.open_task(task_number)
