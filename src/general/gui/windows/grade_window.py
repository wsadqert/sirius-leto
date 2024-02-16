import os
from rich.traceback import install
from typing import Callable
import json

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
	QWidget,                    # the most general classes
	QHBoxLayout, QVBoxLayout,   # layouts
	QPushButton,                # other interactive widgets
	QLabel
)

from src.general.gui.widgets.BottomToolbar import BottomToolbar
from src.general.constants import ASSETS_ROOT

__all__ = ["GradeWidget"]

install(show_locals=True, width=300)
labs = json.load(open(os.path.join(ASSETS_ROOT, "labs_description.json"), encoding="utf-8"))

QAlignment = Qt.AlignmentFlag


class GradeWidget(QWidget):
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
			    background-image: url("assets/background/grade_window.jpg");
			    background-repeat: no-repeat;
			    background-size: 120px;
		    }
		""")

		title_layout = QHBoxLayout()

		back_button = QPushButton()
		back_button.setIcon(QIcon(os.path.join(ASSETS_ROOT, "icons", "arrow_left_in_circle", "arrow_left_in_circle_white_451px.png")))
		back_button.setIconSize(QSize(50, 50))
		back_button.setMaximumWidth(50)
		back_button.clicked.connect(self.back_function)  # noqa (ide error)
		back_button.setStyleSheet("background-color: transparent; ")

		# title
		title_label = QLabel(f"{self.grade_number} класс")
		title_label.setAlignment(QAlignment.AlignLeft | QAlignment.AlignVCenter)
		title_label.setStyleSheet("color: white; font-size: 30px; ")

		# subtitle
		subtitle_label = QLabel("Виртуальные лабораторные работы по физике")
		subtitle_label.setAlignment(QAlignment.AlignRight | QAlignment.AlignVCenter)
		subtitle_label.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 20px; ")

		labs_layout = QVBoxLayout()

		for i, lab in enumerate(labs[str(self.grade_number)]):
			lab_name = lab["title"]

			lab_name_widget = QLabel(f"{i+1}. {lab_name}")
			# lab_name_widget.number = i
			lab_name_widget.setStyleSheet("font-size: 25px; color: #00ff00")
			lab_name_widget.setAlignment(QAlignment.AlignLeft)
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

	def generate_open_task(self, number):
		print('generating open task', number)

		def open_task(_e):
			print('open task', number, _e)
			self.open_task_function((self.grade_number, number))

		return open_task

