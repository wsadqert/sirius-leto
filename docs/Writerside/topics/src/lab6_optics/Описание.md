<script
  src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript">
</script>

# .config

## Структура

Папка `.config` содержит 2 конфигурационных файла:

- [`frontend.cfg`](#настройки-визуальной-части)
- [`raytrace.cfg`](#настройки-движка)

## Настройки визуальной части

Файл может содержать 2 раздела:

- `[tcl]` - настройки `tkinter`, которые будут передавать при создании объекта `Canvas`
- `[Drawer]` - опции кастомизации внешнего вида:
    - `ray_width`: float - ширина линии луча
    - `ray_color`: str - цвет луча

    - `source_size`: float - размер точечных источников света
    - `source_color`: str - цвет заполнения дл точечных источников
    - `source_outline_color`: str - цвет обводки точечных источников

    - `lens_width`: float - видимая толщина линзы
    - `lens_color`: str - цвет линзы

    - `mirror_width`: float - видимая толщина зеркала
    - `mirror_color`: str - цвет зеркала

## Настройки движка
