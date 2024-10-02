import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QRadioButton, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt

__all__ = ["RadioTestPage"]


class RadioTestPage(QWidget):
	def __init__(self, num_radio_buttons: int):
		super().__init__()

		self.init_ui(num_radio_buttons)

	def init_ui(self, num_radio_buttons: int):
		self.setFixedSize(1200, 800)
		self.setWindowTitle("Radio Buttons Example")
		self.setStyleSheet("""
			QRadioButton::indicator {
				border: 1px solid gray;
				height: 22px;
				width: 22px;
				margin: 1px 11px 1px 1px;
				margin-right: 10px;
				border-radius: 12px;
				background: transparent;
			}
			QRadioButton::indicator::checked {
				border: 2px solid #0097e1;
				background: qradialgradient(
	                cx:.5, cy:.5, radius: 0.7,
	                fx:.5, fy:.5,
	                stop:0 #0097e1, 
	                stop:0.45 #0097e1,
	                stop:0.5 transparent,
	                stop:1 transparent
	            );
				margin: 0px 9px 0px 0px;
			}
		""")

		title_label = QLabel("Как правильно делать эксперимент?", self)
		title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		title_label.setStyleSheet("font-size: 60px; color: #333;")
		title_label.setMaximumHeight(80)

		radio_buttons = []
		for i in range(num_radio_buttons):
			radio_button = QRadioButton(f"Radio Button {i + 1}", self)
			radio_button.setStyleSheet("font-size: 24px;")
			radio_button.setFixedHeight(40)
			radio_buttons.append(radio_button)

		vbox_layout = QVBoxLayout()
		vbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
		vbox_layout.setSpacing(10)
		vbox_layout.addStretch()  # Add a spacer before the radio buttons
		for rb in radio_buttons:
			vbox_layout.addWidget(rb)
			vbox_layout.addStretch()  # Add a spacer after the radio buttons

		submit_button = QPushButton("Submit", self)
		submit_button.setStyleSheet("background-color: #00ff00; border-radius: 10px; font-size: 30px;")
		submit_button.setMinimumHeight(50)
		submit_button.setFixedWidth(700)
		submit_button.clicked.connect(self.on_submit_clicked)

		main_layout = QVBoxLayout()
		main_layout.addWidget(title_label)
		main_layout.addLayout(vbox_layout)
		main_layout.addWidget(submit_button, alignment=Qt.AlignmentFlag.AlignHCenter)

		self.setLayout(main_layout)
		self.show()

	def on_submit_clicked(self):
		selected_button_index = -1
		for i, rb in enumerate(self.findChildren(QRadioButton)):
			if rb.isChecked():
				selected_button_index = i
				break

		if selected_button_index != -1:
			print(f"Selected Radio Button: {selected_button_index + 1}")
		else:
			print("No radio button selected")


if __name__ == "__main__":
	app = QApplication(sys.argv)

	num_radio_buttons = 5  # Change this value to set the number of radio buttons

	radio_buttons_app = RadioButtonsApp(num_radio_buttons)

	sys.exit(app.exec())
