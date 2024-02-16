# Класс `TextWithOutline`

Класс предназначен для создания текста с обводкой, как на картинке ниже. 

![](https://www.html-code-generator.com/images/fb/css-text-stroke.png)

```python
class src.general.gui.widgets.TextWithOutline(text, font_color, font_size, outline_color, outline_width)
```

Наследуется от [QtWidgets.QTextEdit](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QTextEdit.html).

## Аргументы
- `text`: str

	Текст для отображения на виджете.
- `font_color`: [Qt.GlobalColor](https://doc.qt.io/qtforpython-6/PySide6/QtCore/Qt.html#PySide6.QtCore.PySide6.QtCore.Qt.GlobalColor)

	Основной цвет текста.
- `font_size`: int

	Размер шрифта в пикселях, которым будет написан текст.
- `outline_color`: [Qt.GlobalColor](https://doc.qt.io/qtforpython-6/PySide6/QtCore/Qt.html#PySide6.QtCore.PySide6.QtCore.Qt.GlobalColor)

	Цвет обводки.
- `outline_width`: int

	Ширина обводки в пикселях. 

## Методы

- ### `alignText`
```python
def alignText(self, alignment: Qt.AlignmentFlag)
```

Выравнивает текст внутри поля согласно переданному аргументу.

### Аргументы

- alignment: [Qt.AlignmentFlag](https://doc.qt.io/qtforpython-6/PySide6/QtCore/Qt.html#PySide6.QtCore.PySide6.QtCore.Qt.AlignmentFlag)

	Способ выравнивания.

### Возвращаемое значение

Нет

