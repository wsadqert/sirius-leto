# Класс `BottomToolbar`

Класс предназначен для создания горизонтальной панели инструментов (тулбара).

```python
class src.general.gui.widgets.BottomToolbar(tools_names, parent=None)
```
Наследуется от [QtWidgets.QWidget](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QWidget.html)

## Аргументы

- `tools_names`: list[str]

	Список инструментов, отображаемых на тулбаре
- `parent`: [QtWidgets.QWidget](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QWidget.html)

	"Родительский" виджет.

## Методы

- ### `BottomToolbar.init_ui`
```python
def BottomToolbar.init_ui(self)
```

Инициализирует макет (layout) для виджета и применяет его. 

#### Аргументы

Нет

#### Возвращаемое значение

Нет

- ### `BottomToolbar.generate_open_tool`

```python
def generate_open_tool(self, tool_name)
```

Создаёт функцию, открывающую инструмент с названием `tool_name` и возвращает её. Название инструмента должно присутствовать в `tools_names`.

#### Аргументы

- `tool_name`: str

	Название инструмента, который требуется открыть.

#### Возвращаемое значение

Нет

## P.S. Вспомогательные классы

Файл также содержит 3 вспомогательных класса:

- `AboutWindow`
- `AboutEquipmentDialog`
- `SuggestImprovementDialog`

Они все наследуются от [QtWidgets.QDialog](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QDialog.html) и представляют собой диалоговые окна, открываемые при вызове того или иного инструмента.