# Класс `Drawer`

Это класс визуализации объектов.

Отвечает за отрисовку геометрических объектов на холсте Tkinter.

## Атрибуты

- `canvas`: tk.Canvas  — холст, на котором производится отрисовка.
- `config`: DrawerConfig | dict  — объект конфигурации, содержащий параметры отрисовки.

Дополнительные атрибуты, добавляемые, если к `canvas`, если они отсутстсвуют:
- `objects`: float  —  список отрисованных объектов.
- `dx_total`: float  — общее смещение по оси X.
- `dy_total`: float  — общее смещение по оси Y.

## Методы

- `Drawer.get_canvas`

```Python
def get_canvas(self) 
```

Возвращает используемый для отрисовки холст.

- `Drawer.draw_ray`

```Python
def draw_ray(self, ray: Ray)
```

Отрисовывает луч [`Ray`](Ray.md) на холсте:

получает начальную и конечную точки луча,
с учётом смещения (`dx_total`, `dy_total`) создаёт линию с параметрами `ray_color` и `ray_width` из конфигурации,
добавляет созданный объект линии в список `canvas.objects`.

- `Drawer.draw_source`

```Python
def draw_source(self, source: Source)
```

Отрисовывает источник [`Source`](abcSource.md) в виде овала:
    
определяет координаты овала, основываясь на координатах источника и его размере `source_size`,
применяет цвета заливки и контура `source_color`, `source_outline_color` из конфигурации,
добавляет созданный овал в список `canvas.objects`.

- `Drawer.draw_lens`

```Python
def draw_lens(self, lens: Lens)
```

Отрисовывает линзу [`Lens`](Lens.md):

вычисляет координаты линии, представляющей линзу, на основе центра, размера `size_y` и угла поворота `angle` линзы,
использует параметры `lens_color` и `lens_width` из конфигурации,
добавляет созданную линию в список `canvas.objects`.

- `Drawer.draw_mirror`

```Python
def draw_mirror(self, mirror: Mirror)
```

Отрисовывает зеркало [`Mirror`](Mirror.md):

вычисляет координаты линии, представляющей зеркало, используя центр (`x`, `y`), размер `size` и угол поворота `angle`,
применяет цвета и толщину линии (`mirror_color`, `mirror_width`) из конфигурации,
добавляет созданный объект линии в список `canvas.objects`.

- `Drawer.draw_component`

```Python
def draw_component(self, component: Component)
```

Отрисовывает компонент, определяемый объектом [`Component`](abcComponent.md).
В зависимости от типа компонента вызывается соответствующий метод отрисовки:

для объекта типа [`Source`](abcSource.md) — вызывается `draw_source`,
для объекта типа [`Lens`](Lens.md) — вызывается `draw_lens`,
для объекта типа [`Mirror`](Mirror.md) — вызывается `draw_mirror`,
для объекта типа [`Wall`](Wall.md) — вызывается `draw_wall`.

Если тип компонента не поддерживается, генерируется исключение `TypeError`.

## Операторы

- `Drawer.__init__`

```Python
def __init__(self, canvas: tk.Canvas, config: DrawerConfig = None)
```

Инициализирует объект Drawer с заданным холстом и конфигурацией отрисовки