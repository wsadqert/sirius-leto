# Класс `Wall`

Наследуется от [`Active`](abcActive.md).

Представляет непроницаемую для световых лучей стенку.

## Атрибуты

- `name`: str — имя компонента.
- `angle`: float — угол компонента в градусах.
- `center`: Point — центр стенки, определяющий его позицию.
- `size`: float — размер стенки по оси y.
- `args`: tuple  — дополнительные позиционные аргументы.
Дополнительные именованные атрибуты задаются через `kwargs`.

## Методы

- `Wall.apply`

```Python
def apply(self, ray: Ray) -> Ray:
```
Поглощает переданный луч [`Ray`](Ray.md), возвращая новый луч с нулевой длиной и с центром в начале координат. 

## Операторы

- `Wall.__init__`

```Python
def __init__(self, name: str, center: Point, size: float, angle: float, *args, **kwargs)
```

Инициализирует стенку, устанавливая:

имя компонента,
центр стенки (на основе объекта [`Point`](Point.md)),
размер, который задается как `size_y` (при этом `size_x` устанавливается равным 0),
угол ориентации в градусах.