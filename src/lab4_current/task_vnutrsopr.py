import random
import sys
from typing import Callable

from PyQt6 import QtCore
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import (
    QApplication, QWidget,  # the most general classes
    QDialogButtonBox,  # dialogs
    QVBoxLayout, QHBoxLayout, QFormLayout,  # layouts
    QLineEdit,  # text boxes
    QPushButton,  # other interactive widgets
    QLabel
)
from bs4 import BeautifulSoup

from src.general.constants import ASSETS_ROOT, ICONS_ROOT
from src.general.gui.dialogs import TextDialog
from src.general.checks import is_positive

__all__ = ["TaskPage"]

QAlignment = Qt.AlignmentFlag


class IncorrectInputDialog(TextDialog):
    def __init__(self, fields: list[str]):
        if len(fields) == 1:
            message = f"Поле <span style='color: red'>{fields[0]}</span> заполнено с ошибкой. Разделителем целой и дробной частей является точка."
        else:
            message = f"Поля <span style='color: red'>{'</span>, <span style=\'color: red\'>'.join(fields)}</span> заполнены с ошибкой. Разделителем целой и дробной частей является точка."

        super().__init__(
            text=message,
            title="Некорректный ввод",
            buttons=QDialogButtonBox.StandardButton.Ok
        )


class TaskPage(QWidget):
    def __init__(self, task_path: str, back_function: Callable):
        super().__init__()

        self.task_path = task_path
        self.back_function = back_function

        self.grade_number = 10

        self.Eds = random.randrange(725, 950, 5) / 100
        self.r = random.randrange(30, 50, 1) / 10
        self.Ramp = random.randrange(15, 25, 1) / 10

        self.correct_answers = [self.Eds, self.r, self.Ramp]
        print(self.correct_answers)

        with open(self.task_path, encoding="utf-8") as f:
            self.task_text = f.read()
        self.soup = BeautifulSoup(self.task_text, 'html.parser')

        '''Sch1_0-Current = Eds/(r+Ra+R) Sch1_1-Current = Eds / (r+Ra) Sch5_0-Current = 0
         Sch3_0-Voltage = Eds Sch6_0-Voltage = 0 Sch6_1-Voltage = Eds/(r+Ra+R)*R '''

        self.setCurrent10(self.Eds,self.r,self.Ramp)
        self.setCurrent11(self.Eds,self.r,self.Ramp)
        self.setCurrent50()
        self.setVoltage30(self.Eds, self.r, self.Ramp)
        self.setVoltage60(self.Eds, self.r, self.Ramp)
        self.setVoltage61()

        # self.title = self.soup.find('h1', {"class": "title"}).string
        self.title = "Определение внутреннего сопротивления и напряжения источника ЭДС"
        self.target_names = ['Напряжение источника', 'Сопротивление источника','Сопротивление амперметра']
        self.units = ['В', 'Ом', 'Ом']

        self.resize(1500, 800)
        self.setWindowTitle("Лаборатория")

        self.init_ui()

    def setCurrent10(self, Eds: float, r: float, Ramp: float):
        new_mathjax = self.soup.new_tag('mathjax', attrs={"class": "Sch1_0-Current"})
        new_mathjax.string = r"I = " + str(round(Eds/(r+4*Ramp),2)) + ' A, '  # + r'$'
        self.soup.find('mathjax', {"class": "Sch1_0-Current"}).replace_with(new_mathjax)
        new_mathjax = self.soup.new_tag('mathjax', attrs={"class": "Sch6_0-Current"})
        new_mathjax.string = r"I = " + str(round(Eds / (r + 4 * Ramp), 2)) + ' A, '  # + r'$'
        self.soup.find('mathjax', {"class": "Sch6_0-Current"}).replace_with(new_mathjax)
        new_mathjax = self.soup.new_tag('mathjax', attrs={"class": "Sch9_0-Current"})
        new_mathjax.string = r"I = " + str(round(Eds / (r + 4 * Ramp), 2)) + ' A, '  # + r'$'
        self.soup.find('mathjax', {"class": "Sch9_0-Current"}).replace_with(new_mathjax)

    def setCurrent11(self, Eds: float, r: float, Ramp: float):
        new_mathjax = self.soup.new_tag('mathjax', attrs={"class": "Sch1_1-Current"})
        new_mathjax.string = r"I = " + str(round(Eds/(r+Ramp),2)) + ' A, '  # + r"$"
        self.soup.find('mathjax', {"class": "Sch1_1-Current"}).replace_with(new_mathjax)
        new_mathjax = self.soup.new_tag('mathjax', attrs={"class": "Sch2_0-Current"})
        new_mathjax.string = r"I = " + str(round(Eds / (r + Ramp), 2)) + ' A, '  # + r"$"
        self.soup.find('mathjax', {"class": "Sch2_0-Current"}).replace_with(new_mathjax)
        new_mathjax = self.soup.new_tag('mathjax', attrs={"class": "Sch2_1-Current"})
        new_mathjax.string = r"I = " + str(round(Eds / (r + Ramp), 2)) + ' A, '  # + r"$"
        self.soup.find('mathjax', {"class": "Sch2_1-Current"}).replace_with(new_mathjax)
        new_mathjax = self.soup.new_tag('mathjax', attrs={"class": "Sch6_1-Current"})
        new_mathjax.string = r"I = " + str(round(Eds / (r + Ramp), 2)) + ' A, '  # + r"$"
        self.soup.find('mathjax', {"class": "Sch6_1-Current"}).replace_with(new_mathjax)
        new_mathjax = self.soup.new_tag('mathjax', attrs={"class": "Sch8_0-Current"})
        new_mathjax.string = r"I = " + str(round(Eds / (r + Ramp), 2)) + ' A, '  # + r"$"
        self.soup.find('mathjax', {"class": "Sch8_0-Current"}).replace_with(new_mathjax)
        new_mathjax = self.soup.new_tag('mathjax', attrs={"class": "Sch8_1-Current"})
        new_mathjax.string = r"I = " + str(round(Eds / (r + Ramp), 2)) + ' A, '  # + r"$"
        self.soup.find('mathjax', {"class": "Sch8_1-Current"}).replace_with(new_mathjax)
        new_mathjax = self.soup.new_tag('mathjax', attrs={"class": "Sch9_1-Current"})
        new_mathjax.string = r"I = " + str(round(Eds / (r + Ramp), 2)) + ' A, '  # + r"$"
        self.soup.find('mathjax', {"class": "Sch9_1-Current"}).replace_with(new_mathjax)
        new_mathjax = self.soup.new_tag('mathjax', attrs={"class": "Sch10_0-Current"})
        new_mathjax.string = r"I = " + str(round(Eds / (r + Ramp), 2)) + ' A, '  # + r"$"
        self.soup.find('mathjax', {"class": "Sch10_0-Current"}).replace_with(new_mathjax)
        new_mathjax = self.soup.new_tag('mathjax', attrs={"class": "Sch10_1-Current"})
        new_mathjax.string = r"I = " + str(round(Eds / (r + Ramp), 2)) + ' A, '  # + r"$"
        self.soup.find('mathjax', {"class": "Sch10_1-Current"}).replace_with(new_mathjax)

    def setCurrent50(self):
        new_mathjax = self.soup.new_tag('mathjax', attrs={"class": "Sch5_0-Current"})
        new_mathjax.string = r"I = 0.00 A, "  # + r"$"
        self.soup.find('mathjax', {"class": "Sch5_0-Current"}).replace_with(new_mathjax)
        new_mathjax = self.soup.new_tag('mathjax', attrs={"class": "Sch5_1-Current"})
        new_mathjax.string = r"I = 0.00 A, "  # + r"$"
        self.soup.find('mathjax', {"class": "Sch5_1-Current"}).replace_with(new_mathjax)
        new_mathjax = self.soup.new_tag('mathjax', attrs={"class": "Sch7_0-Current"})
        new_mathjax.string = r"I = 0.00 A, "  # + r"$"
        self.soup.find('mathjax', {"class": "Sch7_0-Current"}).replace_with(new_mathjax)
        new_mathjax = self.soup.new_tag('mathjax', attrs={"class": "Sch7_1-Current"})
        new_mathjax.string = r"I = 0.00 A, "  # + r"$"
        self.soup.find('mathjax', {"class": "Sch7_1-Current"}).replace_with(new_mathjax)

    def setVoltage30(self, Eds: float, r: float, Ramp: float):
        new_mathjax = self.soup.new_tag('mathjax', attrs={"class": "Sch3_0-Voltage"})
        new_mathjax.string = r"V = " + str(round(Eds,2)) + ' B'  # + r'$'
        self.soup.find('mathjax', {"class": "Sch3_0-Voltage"}).replace_with(new_mathjax)
        new_mathjax = self.soup.new_tag('mathjax', attrs={"class": "Sch3_1-Voltage"})
        new_mathjax.string = r"V = " + str(round(Eds, 2)) + ' B'  # + r'$'
        self.soup.find('mathjax', {"class": "Sch3_1-Voltage"}).replace_with(new_mathjax)
        new_mathjax = self.soup.new_tag('mathjax', attrs={"class": "Sch4_0-Voltage"})
        new_mathjax.string = r"V = " + str(round(Eds, 2)) + ' B'  # + r'$'
        self.soup.find('mathjax', {"class": "Sch4_0-Voltage"}).replace_with(new_mathjax)
        new_mathjax = self.soup.new_tag('mathjax', attrs={"class": "Sch4_1-Voltage"})
        new_mathjax.string = r"V = " + str(round(Eds, 2)) + ' B'  # + r'$'
        self.soup.find('mathjax', {"class": "Sch4_1-Voltage"}).replace_with(new_mathjax)
        new_mathjax = self.soup.new_tag('mathjax', attrs={"class": "Sch5_0-Voltage"})
        new_mathjax.string = r"V = " + str(round(Eds, 2)) + ' B'  # + r'$'
        self.soup.find('mathjax', {"class": "Sch5_0-Voltage"}).replace_with(new_mathjax)
        new_mathjax = self.soup.new_tag('mathjax', attrs={"class": "Sch5_1-Voltage"})
        new_mathjax.string = r"V = " + str(round(Eds, 2)) + ' B'  # + r'$'
        self.soup.find('mathjax', {"class": "Sch5_1-Voltage"}).replace_with(new_mathjax)
        new_mathjax = self.soup.new_tag('mathjax', attrs={"class": "Sch7_0-Voltage"})
        new_mathjax.string = r"V = " + str(round(Eds, 2)) + ' B'  # + r'$'
        self.soup.find('mathjax', {"class": "Sch7_0-Voltage"}).replace_with(new_mathjax)
        new_mathjax = self.soup.new_tag('mathjax', attrs={"class": "Sch7_1-Voltage"})
        new_mathjax.string = r"V = " + str(round(Eds, 2)) + ' B'  # + r'$'
        self.soup.find('mathjax', {"class": "Sch7_1-Voltage"}).replace_with(new_mathjax)
        new_mathjax = self.soup.new_tag('mathjax', attrs={"class": "Sch8_0-Voltage"})
        new_mathjax.string = r"V = " + str(round(Eds, 2)) + ' B'  # + r'$'
        self.soup.find('mathjax', {"class": "Sch8_0-Voltage"}).replace_with(new_mathjax)
        new_mathjax = self.soup.new_tag('mathjax', attrs={"class": "Sch8_1-Voltage"})
        new_mathjax.string = r"V = " + str(round(Eds, 2)) + ' B'  # + r'$'
        self.soup.find('mathjax', {"class": "Sch8_1-Voltage"}).replace_with(new_mathjax)
        new_mathjax = self.soup.new_tag('mathjax', attrs={"class": "Sch9_0-Voltage"})
        new_mathjax.string = r"V = " + str(round(Eds, 2)) + ' B'  # + r'$'
        self.soup.find('mathjax', {"class": "Sch9_0-Voltage"}).replace_with(new_mathjax)
        new_mathjax = self.soup.new_tag('mathjax', attrs={"class": "Sch9_1-Voltage"})
        new_mathjax.string = r"V = " + str(round(Eds, 2)) + ' B'  # + r'$'
        self.soup.find('mathjax', {"class": "Sch9_1-Voltage"}).replace_with(new_mathjax)
        new_mathjax = self.soup.new_tag('mathjax', attrs={"class": "Sch10_0-Voltage"})
        new_mathjax.string = r"V = " + str(round(Eds, 2)) + ' B'  # + r'$'
        self.soup.find('mathjax', {"class": "Sch10_0-Voltage"}).replace_with(new_mathjax)
        new_mathjax = self.soup.new_tag('mathjax', attrs={"class": "Sch10_1-Voltage"})
        new_mathjax.string = r"V = " + str(round(Eds, 2)) + ' B'  # + r'$'
        self.soup.find('mathjax', {"class": "Sch10_1-Voltage"}).replace_with(new_mathjax)
    def setVoltage60(self, Eds: float, r: float, Ramp: float):
        new_mathjax = self.soup.new_tag('mathjax', attrs={"class": "Sch6_0-Voltage"})
        new_mathjax.string = r"V = " + str(round(Eds/(r+1.5*Ramp)*0.5*Ramp,2)) + ' B'  # + r"$"
        self.soup.find('mathjax', {"class": "Sch6_0-Voltage"}).replace_with(new_mathjax)

    def setVoltage61(self):
        new_mathjax = self.soup.new_tag('mathjax', attrs={"class": "Sch6_1-Voltage"})
        new_mathjax.string = r"V = 0.00 В"  # + r"$"
        self.soup.find('mathjax', {"class": "Sch6_1-Voltage"}).replace_with(new_mathjax)

    def init_ui(self):
        layout = QVBoxLayout()

        title_layout = QHBoxLayout()

        back_button = QPushButton()
        back_button.setIcon(QIcon(f"{ICONS_ROOT}\\arrow_left_in_circle\\arrow_left_in_circle_black_451px.png"))
        back_button.setIconSize(QSize(50, 50))
        back_button.setMaximumWidth(50)
        back_button.clicked.connect(lambda _e: self.back_function(self.grade_number)(_e))
        back_button.setStyleSheet("background-color: transparent; ")

        title_label = QLabel(self.title)
        title_label.setStyleSheet("font-size: 30px")
        title_label.setAlignment(QAlignment.AlignCenter)

        columns = QWidget()
        columns_layout = QHBoxLayout()

        web_engine_view = QWebEngineView(columns)
        web_engine_view.setFixedHeight(750)
        web_engine_view.setFixedWidth(900)

        settings = web_engine_view.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AutoLoadImages, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        settings.setUnknownUrlSchemePolicy(QWebEngineSettings.UnknownUrlSchemePolicy.AllowAllUnknownUrlSchemes)

        web_engine_view.setHtml(self.soup.__str__(),
                                QtCore.QUrl.fromLocalFile(rf"{ASSETS_ROOT}\lab4_current\lab4_current.html"))

        form = QWidget(columns)
        form_layout = QFormLayout()
        form.setLayout(form_layout)

        self.inputs: dict[str, QLineEdit] = {}

        # Add input fields to the form
        for name, unit in zip(self.target_names, self.units):
            input1 = QLineEdit()
            input1.setPlaceholderText(unit)
            form_layout.addRow(name, input1)

            self.inputs[name] = input1

        submit_button = QPushButton('Отправить', columns)
        form_layout.addRow(submit_button)

        title_layout.addWidget(back_button)
        title_layout.addWidget(title_label)
        title_widget = QWidget()
        title_widget.setLayout(title_layout)

        columns_layout.addWidget(web_engine_view)
        columns_layout.addWidget(form)
        columns.setLayout(columns_layout)

        submit_button.clicked.connect(self.submit_form)  # noqa (ide error)

        layout.addWidget(title_widget)
        layout.addWidget(columns)

        self.setLayout(layout)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Return:
            self.submit_form()

    def change_border(self, name, state):
        if state:
            border_style = "none"
        else:
            border_style = "2px solid red"
        self.inputs[name].setStyleSheet(f"border: {border_style}")

    def check_correctness(self):
        incorrect_names = []

        for name, val in self.inputs.items():
            is_correct = is_positive(val.text())
            self.change_border(name, is_correct)

            if not is_correct:
                incorrect_names.append(name)

        if incorrect_names:
            IncorrectInputDialog(incorrect_names).show()

        return not len(incorrect_names)

    def check_answers(self):
        # assuming all input fields are filled correctly
        res = [False] * len(self.inputs)
        for i, (_, val) in enumerate(self.inputs.items()):
            if round(float(val.text())) >= round(self.correct_answers[i] * 0.99) and round(float(val.text())) <= round(
                    self.correct_answers[i] * 1.01):
                res[i] = True
        return res

    def submit_form(self):
        if not self.check_correctness():
            return

        res = self.check_answers()
        print(res)

        dialog_text = ""
        correct_text = "<span style='color: green'>Правильно</span>"
        incorrect_text = "<span style='color: red'>Неправильно</span>"
        for i, (name, _) in enumerate(self.inputs.items()):
            dialog_text += f"{name}: {correct_text if res[i] else incorrect_text}<br><br>"

        TextDialog(
            text=dialog_text,
            title="Результат",
            buttons=QDialogButtonBox.StandardButton.Ok
        ).show()


if __name__ == '__main__':
    app = QApplication(sys.argv + ['--no-sandbox'])
    window = TaskPage(f"{ASSETS_ROOT}/lab4_current/lab3_current.html", lambda: ...)
    window.show()

    sys.exit(app.exec())
