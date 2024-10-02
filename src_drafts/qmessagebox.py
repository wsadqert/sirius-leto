import sys

from PyQt6.QtWidgets import QApplication, QMessageBox

app = QApplication(sys.argv)
msg = QMessageBox()
msg.setWindowTitle("title")
msg.setInformativeText("informative")
msg.setText("<h1>text</h1>")
msg.setIcon(QMessageBox.Icon.Critical)

msg.exec()
app.exec()
