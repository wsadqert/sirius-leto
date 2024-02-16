# Низкоуровневые функции

## Функции

- ### `clear_screen`
```python
def clear_screen()
```
Очищает консоль и буфер вывода путём печати "магической" последовательности.

#### Аргументы

Нет

#### Возвращаемые значения

Нет

- ### `sigint_handler`
```python
def sigint_handler(_signal, _frame)
```
Обработчик системного сигнала SIGINT, который инициируется при попытке закрытия программы. 

#### Аргументы

- `_signal`, `_frame` - некие аргументы, передаваемые при вызове обработчика. В коде функции никак не используются.

#### Возвращаемое значение

Нет

- ### `rich_excepthook`
Обработчик исключений, основанный на [`rich.traceback`](https://rich.readthedocs.io/en/stable/traceback.html). Представляет собой незначительно изменённый код из [исходного кода](https://github.com/Textualize/rich/blob/master/rich/traceback.py#L97) библиотеки `rich`.
```python
def rich_excepthook(_event, _type, value, traceback)
```

#### Аргументы

- `_type`: type[BaseException]

	Тип обрабатываемого исключения.
- `value`: BaseException

	Экземпляр исключения.

- `traceback`: Optional[TracebackType]

	Объект `traceback`.

#### Возвращаемое значение

Нет
