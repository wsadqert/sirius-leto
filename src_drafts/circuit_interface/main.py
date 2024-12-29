import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QMessageBox
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtCore import Qt

class Matrix(QWidget):
    def __init__(self):
        super().__init__()

        self.pushed_buttons = []
        self.connected_buttons = []
        self.buttons = {}
        self.init_ui()

    def init_ui(self):
        # Set up the layout
        grid_layout = QGridLayout()

        # Create a 5x5 matrix of buttons
        for row in range(5):
            for col in range(5):
                button = QPushButton(f"({row + 1}, {col + 1})")  # Label each button with its coordinates
                button.clicked.connect(lambda checked, r=row, c=col: self.button_clicked(r, c))
                grid_layout.addWidget(button, row, col)
                self.buttons[(row, col)] = button  # Store button in dictionary

        # Set layout to the main window
        self.setLayout(grid_layout)
        self.setWindowTitle("Circuit Sim")
        self.resize(400, 400)

    def button_clicked(self, row, col):
        print(f"Button clicked at coordinates: ({row + 1}, {col + 1})")

        self.pushed_buttons.append((row, col))  # Store coordinates as tuples

        # Prevent connecting a button to itself
        if len(self.pushed_buttons) > 1 and self.pushed_buttons[-1] == self.pushed_buttons[-2]:
            self.pushed_buttons.pop()

        # Show dialog for every pair of buttons clicked
        if len(self.pushed_buttons) % 2 == 0:
            self.show_confirmation_dialog()

    def show_confirmation_dialog(self):
        # Get the last two buttons
        second_last_button = self.pushed_buttons[-2]
        last_button = self.pushed_buttons[-1]

        # Show a confirmation dialog
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle("Connection")
        msg_box.setText(
            f"Connect these buttons:\n({second_last_button[0] + 1}, {second_last_button[1] + 1}) "
            f"and ({last_button[0] + 1}, {last_button[1] + 1})?"
        )

        # Add custom buttons
        resistor_1_ohm = msg_box.addButton("Resistor 1 Ohm", QMessageBox.ButtonRole.ActionRole)
        resistor_1_kohm = msg_box.addButton("Resistor 1 kOhm", QMessageBox.ButtonRole.ActionRole)
        resistor_1_mohm = msg_box.addButton("Resistor 1 MOhm", QMessageBox.ButtonRole.ActionRole)
        wire_button = msg_box.addButton("Wire", QMessageBox.ButtonRole.ActionRole)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Cancel)

        msg_box.exec()

        if msg_box.clickedButton() == resistor_1_ohm:
            print("1 Ohm resistor selected between", last_button, second_last_button)
        elif msg_box.clickedButton() == resistor_1_kohm:
            print("1000 Ohm resistor selected between", last_button, second_last_button)
        elif msg_box.clickedButton() == resistor_1_mohm:
            print("1000000 Ohm resistor selected between", last_button, second_last_button)
        elif msg_box.clickedButton() == wire_button:
            print("Wire selected between", last_button, second_last_button)


app = QApplication(sys.argv)
window = Matrix()
window.show()
app.exec()