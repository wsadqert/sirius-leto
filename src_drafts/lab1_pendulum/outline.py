from PyQt6.QtWidgets import *
import sys
from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextDocument, QTextCursor
from PyQt6.QtGui import QColor, QPainter, QPainterPath, QBrush, QPen, QPalette, QFont


class MyTextDocument(QTextDocument):
	def __init__(self, parent, font):
		super().__init__()

		self.parent = parent

		self.setDefaultFont(font)

	def drawContents(self, painter):
		super().drawContents(painter)

		my_cursor = self.parent.textCursor()
		my_char_format = my_cursor.charFormat()

		my_char_format.setTextOutline(QPen(Qt.GlobalColor.red, 5))
		my_cursor.select(QTextCursor.SelectionType.Document)
		my_cursor.mergeCharFormat(my_char_format)

		super().drawContents(painter)

		my_char_format.setTextOutline(QPen(Qt.GlobalColor.transparent))
		my_cursor.mergeCharFormat(my_char_format)

		super().drawContents(painter)


class MyTextEdit(QTextEdit):
	def __init__(self):
		super().__init__()

		font = self.currentFont()
		font.setPointSize(80)
		font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)

		# self.setDocument(MyTextDocument(self, font))
		self.setHtml("<p style='text-stroke: 2px cyan'>Does it work?</p>")

		self.setText()
		self.resize(800, 400)

	def paintEvent(self, event):
		painter = QPainter(self.viewport())

		super(MyTextEdit, self).paintEvent(event)

		self.document().drawContents(painter)


if __name__ == '__main__':
	app = QApplication(sys.argv)

	win = MyTextEdit()
	win.show()

	app.exec()
