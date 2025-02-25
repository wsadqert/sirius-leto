# Класс `Component`

Наследуется от класса `ABC` одноимённой библиотеки.

Представляет абстрактный компонент с именем, позицией, углом поворота и размерами.

## Атрибуты

- `name`: str — имя компонента.
- `x`: float — x-координата вектора.
- `y`: float — y-координата вектора.
- `angle`: float — угол компонента в градусах.
- `size_x`: float — размер компонента по оси x.
- `size_y`: float — размер компонента по оси y.
- `args`: tuple  — дополнительные позиционные аргументы.
  Дополнительные именованные атрибуты задаются через `kwargs`.

## Методы

- `Component.get_points`

```Python
def get_points(self) -> list[Point]
```

Абстрактный метод, который должен быть реализован в наследниках.
Возвращает список точек [`Point`](Point.md), определяющих геометрию компонента.

- `Component.to_segment`

```Python
def to_segment(self) -> Segment
```
Преобразует компонент в объект [`Segment`](Segment.md) на основе точек, возвращаемых методом `self.get_points`.

- `Component.point`

```Python
def point(self)
```

Возвращает объект [`Point`](Point.md) с координатами компонента (`x`, `y`).

- `Component.size`

```Python
def size(self) -> float
```

Возвращает размер (во `float`) компонента, вычисляемый как евклидова норма вектора (`self.size_x`, `self.size_y`).

## Операторы

- `Component.__init__`

```Python
def __init__(self, name: str, point: Point, angle: float, size_x: float, size_y: float, *args, **kwargs):
```

Инициализирует компонент, устанавливая имя, координаты (на основе переданной точки [`Point`](Point.md)), угол и размеры. Дополнительные аргументы сохраняются в `args` и устанавливаются через `kwargs`.
