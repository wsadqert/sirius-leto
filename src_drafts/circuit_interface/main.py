import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QMessageBox
from PyQt6.QtGui import QPainter, QPixmap, QTransform, QIcon
from PyQt6.QtCore import Qt, QSize
import math

class Matrix(QWidget):
    def __init__(self):
        super().__init__()

        self.pushed_buttons = []
        self.connected_buttons = []
        self.buttons = {}
        self.connections = []  # Список для хранения соединений
        self.images = {
            '1ohm': QPixmap('Res1Ohm.png'),
            '1kohm': QPixmap('Res1kOhm.png'),
            '1mohm': QPixmap('Res1mOhm.png'),
            'wire': QPixmap('Wire.png')
        }  # Словарь для хранения изображений
        self.init_ui()

    def init_ui(self):
        grid_layout = QGridLayout()

        for row in range(7):
            for col in range(11):
                button = QPushButton()  # Убрали текст
                button.setFixedSize(80, 60)  # Фиксированный размер
                # Стиль с фоновым изображением
                button.setStyleSheet("""
                    QPushButton {
                        background-image: url(button.png);
                        background-repeat: no-repeat;
                        background-position: center;
                        border: none;
                    }
                """)
                button.clicked.connect(lambda checked, r=row, c=col: self.button_clicked(r, c))
                grid_layout.addWidget(button, row, col)
                self.buttons[(row, col)] = button

        self.setLayout(grid_layout)
        self.setWindowTitle("Circuit Sim")
        self.resize(800, 500)  # Увеличил размер окна для 11x7 кнопок

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Туториал")
        msg_box.setText(
            "Вы в симуляторе макетной платы. Черные точки - гнезда для соединения. Добавить элемент можно, щелкнув на две черные точки. Соединять можно только соседние гнезда"
        )
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)

        msg_box.exec()

    def button_clicked(self, row, col):
        print(f"Button clicked at coordinates: ({row + 1}, {col + 1})")
        self.pushed_buttons.append((row, col))

        if len(self.pushed_buttons) > 1 and self.pushed_buttons[-1] == self.pushed_buttons[-2]:
            self.pushed_buttons.pop()

        if len(self.pushed_buttons) % 2 == 0:
            self.show_confirmation_dialog()

    def show_confirmation_dialog(self):
        second_last_button = self.pushed_buttons[-2]
        last_button = self.pushed_buttons[-1]

        if abs(last_button[0]-second_last_button[0])<=1 and abs(last_button[-1]-second_last_button[-1])<=1:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle("Connection")
            msg_box.setText(
                f"Соединим ячейки:\n({second_last_button[0] + 1}, {second_last_button[1] + 1}) "
                f"и ({last_button[0] + 1}, {last_button[1] + 1})?"
            )

            resistor_1_ohm = msg_box.addButton("Resistor 1 Ohm", QMessageBox.ButtonRole.ActionRole)
            resistor_1_kohm = msg_box.addButton("Resistor 1 kOhm", QMessageBox.ButtonRole.ActionRole)
            resistor_1_mohm = msg_box.addButton("Resistor 1 MOhm", QMessageBox.ButtonRole.ActionRole)
            wire_button = msg_box.addButton("Wire", QMessageBox.ButtonRole.ActionRole)
            msg_box.setStandardButtons(QMessageBox.StandardButton.Cancel)

            msg_box.exec()

            # Обработка выбора пользователя
            if msg_box.clickedButton() == resistor_1_ohm:
                self.connections.append({
                    'start': second_last_button,
                    'end': last_button,
                    'type': '1ohm'
                })
                self.update()
            elif msg_box.clickedButton() == resistor_1_kohm:
                self.connections.append({
                    'start': second_last_button,
                    'end': last_button,
                    'type': '1kohm'
                })
                self.update()
            elif msg_box.clickedButton() == resistor_1_mohm:
                self.connections.append({
                    'start': second_last_button,
                    'end': last_button,
                    'type': '1mohm'
                })
                self.update()
            elif msg_box.clickedButton() == wire_button:
                self.connections.append({
                    'start': second_last_button,
                    'end': last_button,
                    'type': 'wire'
                })
                self.update()
        else:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle("Connection")
            msg_box.setText("Вы можете соединить только соседние ячейки.")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        for connection in self.connections:
            start_button = self.buttons.get(connection['start'])
            end_button = self.buttons.get(connection['end'])

            if start_button and end_button:
                # Получаем координаты центров кнопок относительно главного окна
                start_center = start_button.mapTo(self, start_button.rect().center())
                end_center = end_button.mapTo(self, end_button.rect().center())

                dx = end_center.x() - start_center.x()
                dy = end_center.y() - start_center.y()
                length = math.hypot(dx, dy)

                if length == 0:
                    continue

                image = self.images.get(connection['type'])
                if image and not image.isNull():
                    # Вычисляем угол поворота
                    angle_rad = math.atan2(dy, dx)
                    angle_deg = math.degrees(angle_rad)

                    # Создаем трансформацию
                    transform = QTransform()

                    # Перемещаем в начальную точку
                    transform.translate(start_center.x(), start_center.y())

                    # Поворачиваем систему координат
                    transform.rotate(angle_deg)

                    # Масштабируем изображение по длине соединения
                    scale_factor = length / image.width()
                    transform.scale(scale_factor, 1)

                    # Центрируем изображение по вертикали
                    transform.translate(0, -image.height() / 2)

                    # Применяем трансформацию
                    painter.setTransform(transform)
                    painter.drawPixmap(0, 0, image)
                    painter.resetTransform()


app = QApplication(sys.argv)
window = Matrix()
window.show()
app.exec()