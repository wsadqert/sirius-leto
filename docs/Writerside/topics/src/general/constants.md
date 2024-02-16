# Глобальные константы

## Переменные

- `os`: module

	_Импортировано из `os`_
- `sys`: module

	_Импортировано из `sys`_
- `perf_counter`: Callable

	_Импортировано из `time.perf_counter`_
- `real_time`: Callable

	_Импортировано из `time.time`_
- `g`: float

	_Импортировано из `scipy.constants.g`_
- `pi`: float

	_Импортировано из `math.pi`_
- `PROJECT_ROOT`: str
	
	Корневой каталог проекта.
- `DATASTORE_ROOT`: str

	Корневой каталог хранилища временных данных.
- `ASSETS_ROOT`: str

	Корневой каталог хранилища внешних ресурсов.


## Функции

- ### `sleep`

```python
def sleep(duration)
```
Аналог `time.sleep` с повышенной точностью (до 100 нс).

#### Аргументы

- `duration`: float

Требуемая продолжительность "сна".

#### Возвращаемые значения

Нет