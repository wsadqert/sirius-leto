# Класс `Active`

Наследуется от [`Component`](abcComponent.md).

Представляет абстрактный активный компонент, который может модифицировать лучи.
Класс предназначен для реализации эффектов, влияющих на прохождение лучей через компонент.

## Атрибуты

- `name`: str — имя компонента.
- `x`: float — x-координата вектора.
- `y`: float — y-координата вектора.
- `angle`: float — угол компонента в градусах.
- `size_x`: float — размер компонента по оси x.
- `size_y`: float — размер компонента по оси y.
- `args`: tuple — дополнительные позиционные аргументы.
  Дополнительные именованные атрибуты задаются через `kwargs`.

## Методы

- `Active.apply`

```Python
def apply(self, ray: Ray) -> Ray:
```

Абстрактный метод, предназначенный для применения эффекта или модификации переданного луча (Ray).

- `Active.distance`

```Python
def distance(self, point: Point) -> float:
```
Вычисляет и возвращает минимальное расстояние от заданной точки до отрезка, представляющего компонент.
Для расчёта используется функция `calculate_point_segment_distance` из модуля `geometry`.

- `Active.get_points`

```Python
def get_points(self) -> tuple[Point, Point]
```
Вычисляет и возвращает кортеж из двух точек [`Point`](Point.md), определяющих отрезок, ассоциированный с компонентом.
Возвращает кортеж из двух объектов [`Point`](Point.md) с координатами (`xi`, `yi`), i = 1,2.

## Операторы

- `Active.__init__`

```Python
def __init__(self, name: str, point: Point, size_x: float, size_y: float, angle: float, *args, **kwargs)
```
Инициализирует активный компонент, устанавливая имя, позицию (на основе объекта [`Point`](Point.md)),
размеры и угол компонента, а также передавая дополнительные аргументы в базовый класс.

