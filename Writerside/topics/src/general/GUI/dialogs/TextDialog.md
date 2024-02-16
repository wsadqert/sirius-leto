# Класс `TextDialog`

Класс предназначен для создания простых диалоговых окон, содержащих только 1 надпись (объект класса [QLabel](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QLabel.html)).

```python
class src.general.gui.dialogs.TextDialog(text="", title="", buttons=QDialogButtonBox.StandardButton.Close)
```
Наследуется от [QtWidgets.QDialog](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QDialog.html).

## Аргументы
- `text`: str

	Текст, который будет отображён внутри диалогового окна.
- `title`: str
	
	Заголовок созданного окна.
- `buttons`: [QDialogButtonBox.StandardButton](https://doc.qt.io/qt-6/qdialogbuttonbox.html#StandardButton-enum)

	Кнопка, которая будет находиться внизу окна. Разрешается совмещать несколько кнопок с помощью опреатора pipe (`|`). 
	
	Например:
	
	```python
 	TextDialog("Lorem", "Ipsum", QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
	```

## Методы

- ### `TextDialog.show`
```python
def TextDialog.show()
```

Алиас для `TextDialog.exec()` (унаследовано от [QtWidgets.QDialog](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QDialog.html)). "Выполняет" виджет, то есть отображает диалоговое окно, блокируя его до тех пор, пока пользователь не закроет его.

#### Аргументы
Нет

#### Возвращаемое значение
Тип: `int`

Код, обозначающий выбор пользователя в случае нескольких кнопок. Может принимать 2 значения, которые определяются [`QtWidgets.QDialog.DialogCode`](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QDialog.html#PySide6.QtWidgets.PySide6.QtWidgets.QDialog.DialogCode):
- `QtWidgets.QDialog.Accepted`
- `QtWidgets.QDialog.Rejected`