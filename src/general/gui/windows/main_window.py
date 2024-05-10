import os
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
	QApplication, QMainWindow, QWidget,  # the most general classes
	QHBoxLayout, QVBoxLayout,   # layouts
	QLabel
)

from src.general.gui.windows.task_page import TaskPage
from src.general.gui.widgets import BottomToolbar, TextWithOutline
from .grade_page import GradePage

__all__ = ["MainWindow", "start"]

QAlignment = Qt.AlignmentFlag


class MainWindow(QMainWindow):
	"""
	The MainWindow class is responsible for creating and managing the main window of the application.
	It contains the layout and widgets for the title, grades, and toolbar.

	Attributes:
		grades_widget (QWidget): The widget that contains the layout for the grades.
		toolbar (BottomToolbar): The toolbar widget for the main window.

	Methods:
		__init__(self): Initializes the MainWindow and sets its fixed size and window title.
		init_ui(self): Initializes the user interface elements, including the title, grades, and toolbar.
		generate_open_grade(self, grade_number): Generates a function that opens a grade page when a grade button is clicked.
		set_task(self, task_number: tuple[int, int]): Sets the task number and updates the central widget with the corresponding task page.
	"""

	def __init__(self):
		"""
		Initializes the MainWindow and sets its fixed size and window title.
		"""
		super().__init__()

		self.setFixedSize(1200, 800)
		self.setWindowTitle("Главное окно")

		self.init_ui()

	def init_ui(self):
		"""
		Initializes the user interface elements, including the title, grades, and toolbar.

		:return: None
		"""
		setBackground(True)

		# title
		title_label = TextWithOutline("Виртуальные лабораторные работы\n по физике", Qt.GlobalColor.white, 50, Qt.GlobalColor.black, 10)
		title_label.alignText(QAlignment.AlignCenter)
		title_label.setStyleSheet("background-color: transparent; border: none")  # noqa (ide error)
		title_label.setMaximumHeight(190)

		# big buttons with grades
		grades_layout = QHBoxLayout()
		grades_layout.setSpacing(20)
		self.grades_widget = QWidget()
		self.grades_widget.setLayout(grades_layout)

		for i in range(8, 12):
			# "N класс" text
			grade_text = QLabel(f"{i} класс")
			grade_text.setStyleSheet("font-size: 45px;")
			grade_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
			grade_text.setMaximumHeight(40)

			# picture
			grade_pic = QLabel()
			grade_pic.setAlignment(Qt.AlignmentFlag.AlignCenter)
			path2pic = os.path.join("assets", "background", f"grade_{i}.png")
			if os.path.exists(path2pic):
				grade_pic.setPixmap(QPixmap(path2pic).scaledToWidth(220))
			else:
				print(f"Warning: path {path2pic} does not exist")

			# big button widget init
			grade_widget_layout = QVBoxLayout()
			grade_widget_layout.addSpacing(25)
			grade_widget_layout.addWidget(grade_text)
			grade_widget_layout.addWidget(grade_pic)

			grade_widget = QWidget()
			grade_widget.setLayout(grade_widget_layout)
			grade_widget.setStyleSheet("""
				border-radius: 25px;
				background-color: #d9d9d9;
			""")
			grade_widget.setMaximumHeight(300)
			grade_widget.mouseReleaseEvent = self.generate_open_grade(i)
			grades_layout.addWidget(grade_widget)

		# toolbar
		self.toolbar = BottomToolbar(self)

		# layout of window
		layout = QVBoxLayout()
		layout.addSpacing(50)
		layout.addWidget(title_label)
		layout.addWidget(self.grades_widget)
		layout.addWidget(self.toolbar)

		self.central_widget = QWidget()
		self.central_widget.setLayout(layout)
		self.setCentralWidget(self.central_widget)

	def generate_open_grade(self, grade_number):
		"""
		Generates a function that opens a grade page when a grade button is clicked.

		:param grade_number: The number of the grade to be opened.
		:return: A function that opens a grade page when called.
		"""
		def open_grade(_event=...):
			grade_n_widget = GradePage(grade_number, self.init_ui, self.set_task)
			self.setCentralWidget(grade_n_widget)

		return open_grade

	def set_task(self, task_number: tuple[int, int]):
		"""
		Sets the task number and updates the central widget with the corresponding task page.

		:param task_number: A tuple containing the task number and its index.
		:return: None
		"""
		print(task_number, task_number[1])
		task_widget = TaskPage(task_number, self.generate_open_grade)
		self.setCentralWidget(task_widget)
		setBackground(False)


def start():
	"""
    Initializes the application and displays the main window.

	:return: None
	"""
	global app
	app = QApplication(sys.argv)
	app.setStyleSheet("""
		MainWindow {
			background-repeat: no-repeat;
		}
	""")
	setBackground(True)

	window = MainWindow()
	window.show()

	sys.exit(app.exec())


def setBackground(flag: bool):
	"""
	Sets the background image for the MainWindow.

	:param flag: A boolean value that determines whether to set the background image.
	:return: None
	"""
	style = "MainWindow { background-image: "
	if flag:
		style += 'url("assets/background/main_window.jpg")'
	else:
		style += 'none'

	style += '; }'
	app.setStyleSheet(style)


if __name__ == "__main__":
	start()
