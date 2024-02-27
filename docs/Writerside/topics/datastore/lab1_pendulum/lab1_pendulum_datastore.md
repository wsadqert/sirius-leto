# Лаборатория №1. Физический маятник.

Внутри `/datastore/lab1_pendulum/` находится 1 файл:

`last_run_log.log` - содержит журнал работы программы. 

Формат:
```
[dd/mm/yyyy hh:mm:ss] TYPE   MESSAGE   filename.py:line
```

- `[dd/MM/yyyy hh:mm:ss.tttttt]` - текущее время;
  - `dd` - текущий день,
  - `MM` - текущий месяц,
  - `yyyy` - текущий год,
  - `hh` - текущий час,
  - `mm` - текущая минута,
  - `ss` - текущая секунда,
  - `tttttt` - текущая микросекунда (дробная часть секунд с точностью до микросекунд),
- `TYPE` - тип сообщения (`DEBUG`/`INFO`/`WARNING`/`ERROR`/`CRITICAL`);
- `MESSAGE` - текст сообщения;
- `filename.py` - имя файла, из которого была вызвана функция логгирования;
- `line` - номер строки в файле `filename.py`, содержащей вызов записи в лог.

Пример записи в журнале:
```
[01/01/2024 17:17:01.085765] INFO   Setting up tkinter   animate.py:139
```