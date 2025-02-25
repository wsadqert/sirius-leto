# Модуль `geometry`

Модуль содержит набор функций для вычислений и операций с геометрическими объектами (точки, лучи, отрезки).

## Методы

- `calculate_ray_direction`

```Python
def calculate_ray_direction(ray: Ray) -> Vector
```

Вычисляет нормализованный направляющий вектор для заданного объекта [`Ray`](Ray.md).
Возвращает получившийся нормализованный [`Vector`](Vector.md).
Если длина луча равна 0, возвращается нулевой вектор.

- `ray_segment_intersection`

```Python
def ray_segment_intersection(segment: Segment, ray: Ray) -> Point | None
```
Определяет точку пересечения между лучом [`Ray`](Ray.md) и отрезком [`Segment`](Segment.md).
Возвращает [`Point`](Point.md) — точка пересечения, если луч пересекает отрезок, иначе `None`.

- `calculate_point_segment_distance`

```Python
def calculate_point_segment_distance(point: Point, segment: Segment) -> float
```

Вычисляет минимальное евклидово расстояние (во `float`) от заданной точки [`Point`](Point.md) до отрезка [`Segment`](Segment.md).

- `iterate_over_length`

```Python
def iterate_over_length(segment: Segment, step: float = None, num_steps: int = None, direction: int = 1) -> Generator[tuple[int, Point], None, None]
```

Итерирует по точкам вдоль отрезка [`Segment`](Segment.md) с заданным шагом `step` (во `float`) или количеством шагов `num_steps` (в `int`).
Оба параметры по умолчанию равны `None`. 
`direction` (в `int`) — направление итерации. По умолчанию равен 1. Допустимые значения: 1 или -1.

Возвращает `Generator[tuple[int, Point], None, None]` — генератор, который на каждой итерации возвращает кортеж, содержащий

порядковый номер шага (целое число);
объект [`Point`](Point.md), соответствующий вычисленной точке на отрезке.