from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPainter, QPen, QTextCursor, QTextDocument
from PyQt6.QtWidgets import *

__all__ = ["TextWithOutline"]
QAlignment = Qt.AlignmentFlag


class MyTextDocument(QTextDocument):
	def __init__(self, parent, font: QFont, outline_color: Qt.GlobalColor = Qt.GlobalColor.red, outline_width: int = 5):
		super().__init__()

		self.parent = parent
		self.outline_color = outline_color
		self.outline_width = outline_width

		self.setDefaultFont(font)

	def drawContents(self, painter):
		super().drawContents(painter)

		cursor = self.parent.textCursor()
		char_format = cursor.charFormat()

		char_format.setTextOutline(QPen(self.outline_color, self.outline_width))
		cursor.select(QTextCursor.SelectionType.Document)
		cursor.mergeCharFormat(char_format)

		super().drawContents(painter)

		char_format.setTextOutline(QPen(Qt.GlobalColor.transparent))
		cursor.mergeCharFormat(char_format)

		super().drawContents(painter)


class TextWithOutline(QTextEdit):
	def __init__(self, text: str, font_color: Qt.GlobalColor = None, font_size: int = None, outline_color: Qt.GlobalColor = None, outline_width: int = None):
		super().__init__()

		self.text = text

		font = self.currentFont()
		font.setPointSize(font_size)
		font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
		self.setDocument(MyTextDocument(self, font, outline_color, outline_width))

		self.setTextColor(font_color)
		self.setText(text)
		self.setDisabled(True)

	def alignText(self, alignment: QAlignment):
		cursor = self.textCursor()

		for i in self.text.split('\n'):
			self.setAlignment(alignment)
			cursor.movePosition(QTextCursor.MoveOperation.Right, n=len(i) + 1)
			self.setTextCursor(cursor)

	def paintEvent(self, event):
		painter = QPainter(self.viewport())

		super(TextWithOutline, self).paintEvent(event)

		self.document().drawContents(painter)


# win = TextWithOutline("Text", 100, Qt.GlobalColor.cyan, 10)  # example
