from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QLabel, QListWidget, QMainWindow, QVBoxLayout, QWidget

from src.general.constants import BIBLIOGRAPHY, ICONS_ROOT

__all__ = ["BibliographyWindow"]


def _get_bibliography():
	with open(BIBLIOGRAPHY, encoding="utf-8") as f:
		return [i.strip() for i in f.readlines()]


class BibliographyWindow(QMainWindow):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.init_ui()

	def init_ui(self):
		self.setFixedSize(700, 400)
		self.setWindowTitle("Список литературы")
		self.setWindowIcon(QIcon(f"{ICONS_ROOT}\\book\\book_20.png"))

		# this line ↓ raises a `TypeError: invalid argument to sipBadCatcherResult()`
		# it could be fixed by using regular function instead of lambda
		self.keyPressEvent = lambda _event: self.close() if _event.key() == Qt.Key.Key_Escape else None

		central_widget = QWidget()
		layout = QVBoxLayout()

		heading = QLabel("Список литературы")
		heading.setStyleSheet("font-size: 25px; font-weight: bold")
		heading.setAlignment(Qt.AlignmentFlag.AlignCenter)

		self.names_list = QListWidget()
		self.names_list.addItems(_get_bibliography())

		self.names_list.setStyleSheet("""
			QListView {
				font-size: 15px;
				color: black;
			}
			QListView::item {
				margin-top: 5px;
				margin-bottom: 5px;
				height: 50px;
			}
		""")

		layout.addWidget(heading)
		layout.addWidget(self.names_list)

		central_widget.setLayout(layout)
		self.setCentralWidget(central_widget)
