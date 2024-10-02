from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QLabel, QMainWindow, QPushButton, QStackedWidget, QVBoxLayout, QWidget, QListWidget, QListWidgetItem
from PyQt6.QtCore import QModelIndex, QSize, Qt
from PyQt6.QtWebEngineWidgets import QWebEngineView

import os
from rich.traceback import install

from src.general.gui.key_handler import _handle_key_gen
from src.general.constants import ASSETS_ROOT, ICONS_ROOT, QLISTVIEW_STYLE

__all__ = ["TextTaskListWindow"]

install(show_locals=True, width=300)

with open(f"{ASSETS_ROOT}\\taskbook\\taskbook.txt") as f:
	names = [x.strip() for x in f.readlines()]
# names = [f"{i + 1}. {name}" for i, name in enumerate(names)]


class TaskPage(QWidget):
	def __init__(self, task_item: int):
		super().__init__()
		self.task_item = task_item

		self.init_ui()

	def init_ui(self):
		layout = QVBoxLayout()

		self.back_button = QPushButton(text="Назад")
		back_icon = QIcon(f"{ICONS_ROOT}\\arrow_left_in_circle\\arrow_left_in_circle_black_451px.png")
		self.back_button.setIcon(back_icon)
		self.back_button.setIconSize(QSize(20, 20))
		self.back_button.setStyleSheet(
			"""
			background-color: #d9d9d9;
			border-radius: 5px;
			font-weight: bold;
			padding: 5px;
			color: black;
			text-align: center;
			cursor: pointer;
			"""
		)
		self.web_engine_view = QWebEngineView()

		path = f"{ASSETS_ROOT}\\taskbook\\{self.task_item + 1}.html"

		if os.path.exists(path):
			with open(path) as f:
				self.web_engine_view.setHtml(f.read())
		else:
			self.web_engine_view.setHtml(f"<h1>Not found: {path}</h1>")

		layout.addWidget(self.back_button)
		layout.addWidget(self.web_engine_view)
		self.setLayout(layout)


class MainPage(QWidget):
	"""
	List of tasks
	"""
	def __init__(self):
		super().__init__()
		self.init_ui()

	def init_ui(self):
		layout = QVBoxLayout()

		heading = QLabel("Задачи на математический маятник")
		heading.setStyleSheet("font-size: 40px; font-weight: bold")
		heading.setAlignment(Qt.AlignmentFlag.AlignCenter)

		self.names_list = QListWidget()
		self.names_list.addItems(names)

		with open(QLISTVIEW_STYLE) as f:
			self.names_list.setStyleSheet(f.read().strip())

		layout.addWidget(heading)
		layout.addWidget(self.names_list)
		self.setLayout(layout)


class TextTaskListWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.init_ui()

	def init_ui(self):
		self.resize(800, 620)
		self.setWindowTitle("Задачник")

		self.stackedWidget = QStackedWidget()

		self.main_page = MainPage()
		self.main_page.names_list.itemClicked.connect(self._handle_item_click)
		self.main_page.names_list.activated.connect(self._handle_item_enter)

		self.stackedWidget.addWidget(self.main_page)
		for i, name in enumerate(names):
			task_page = TaskPage(i)
			task_page.keyPressEvent = _handle_key_gen(Qt.Key.Key_Backspace, self.go_to_main)
			task_page.back_button.clicked.connect(self.go_to_main)
			self.stackedWidget.addWidget(task_page)

		self.go_to_main()

		self.setCentralWidget(self.stackedWidget)

		self.keyPressEvent = _handle_key_gen(Qt.Key.Key_Escape, self.close)

	def go_to_main(self):
		self.stackedWidget.setCurrentIndex(0)

	def _handle_item_click(self, item: QListWidgetItem):
		self.go_to_task(self.main_page.names_list.row(item))

	def _handle_item_enter(self, item: QModelIndex):
		self.go_to_task(item.row())

	def go_to_task(self, item_index):
		self.stackedWidget.setCurrentIndex(item_index + 1)

	def exec(self):
		self.show()
