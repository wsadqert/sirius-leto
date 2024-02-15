from PyQt6.QtWidgets import (
	QDialog, QDialogButtonBox,  # dialogs
	QVBoxLayout,                # layouts
	QLabel
)

__all__ = ["TextDialog"]


class TextDialog(QDialog):
	def __init__(self, text: str = "Lorem ipsum", title: str = "Отправлено!", buttons: QDialogButtonBox.StandardButton = QDialogButtonBox.StandardButton.Close):
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
		self.exec()
