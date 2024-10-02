from PyQt6.QtWidgets import (
	QDialog, QDialogButtonBox,  # dialogs
	QVBoxLayout,                # layouts
	QLabel
)

__all__ = ["TextDialog"]


class TextDialog(QDialog):
	"""
	A custom dialog class that displays a text and buttons.

	Methods:
	- `__init__(self, text, title, buttons)`: Initializes the dialog with the given text, title, and buttons type.
	- `show(self)`: Displays the dialog and waits for the user to interact with it. Returns True if the user accepts the dialog, False otherwise.
	"""

	def __init__(self, text: str, title: str, buttons: QDialogButtonBox.StandardButton = QDialogButtonBox.StandardButton.Close):
		"""
		Initializes the dialog with the given text, title, and buttons.

		:param text: Text displayed in the dialog.
		:param title: Title of window.
		:param buttons:
		"""
		super().__init__()

		self.setWindowTitle(title)

		self.buttonBox = QDialogButtonBox(buttons)
		self.buttonBox.rejected.connect(self.reject)  # noqa (ide error)
		self.buttonBox.accepted.connect(self.accept)  # noqa (ide error)

		self.layout = QVBoxLayout()
		self.layout.addWidget(QLabel(text))
		self.layout.addWidget(self.buttonBox)
		self.setLayout(self.layout)

	def show(self):
		return self.exec()
