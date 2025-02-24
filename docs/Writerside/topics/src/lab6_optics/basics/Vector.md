# Класс `Vector`

Наследуется от [`Basic2D`](Basic2D.md).

Класс Vector представляет радиус-вектор из начала координат на 2D-плоскости.

## Атрибуты

- `x`: float — x-координата вектора
- `y`: float — y-координата вектора

## Методы

- `Vector.rotate`

```Python
def rotate(self, angle: float) -> "Vector"
```

Поворачивает вектор против часовой стрелки на заданный угол (в градусах).
Возвращает новый экземпляр класса `Vector`.

- `Vector.from_points`

```Python
def from_points(cls, point_1: Point, point_2: Point)
```
Метод класса, создаёт экземпляр радиус-вектора по разности координат между двум заданными точками [`Point`](Point.md).

- `Vector.from_segment`

```Python
def from_segment(cls, segment: Segment)
```

Метод класса, создает вектор на основе разности точек отрезка [`Segment`](Segment.md).

- `Vector.from_angle`

```Python
def from_point(cls, point: Point)
```

Метод класса, создает вектор из координат одной точки [`Point`](Point.md).

- `Vector.from_polar`

```Python
def from_polar(cls, length: float, angle: float)
```

Метод класса, создает вектор по полярным координатам, используя длину и угол (в градусах).

- `Vector.get_points`

```Python
def get_points(self)
```

Геттер, возвращает список с одним объектом [`Point`](Point.md) (конечная точка радиус-вектора).

## Операторы

- `Vector.__neg__`

```Python
def __neg__(self) -> "Vector":
```

Возвращает новый объект `Vector`, повёрнутый на 180 градусов.

- `Vector.__add__`

```Python
def  __add__(self, other: Union["Vector", Point]) -> "Vector"
```

Реализует операцию сложения с переданным объектом ([`Point`](Point.md) или `Vector`)
Возвращает новый объект `Vector`, заданный суммой соответствующих координат.

- `Vector.__radd__`

```Python
def  __radd__(self, other: Point) -> "Vector"
```

Поддерживает операцию сложения, когда вектор находится справа.
Возвращает новый объект `Vector`, заданный суммой соответствующих координат.

- `Vector.__sub__`

```Python
def __sub__(self, other: Union["Vector", Point]) -> "Vector"
```

Реализует операцию вычитания с переданным объектом ([`Point`](Point.md) или `Vector`)
Возвращает новый объект `Vector`, заданный разностью соответствующих координат.

- `Vector.__rsub__`

```Python
def  __rsub__(self, other: Point) -> "Vector"
```

Поддерживает операцию вычитания, когда вектор находится справа.
Возвращает новый объект `Vector`, заданный разностью соответствующих координат.

- `Vector.__mul__`

```Python
def  __mul__(self, scalar: float) -> "Vector"
```

Реализует умножение вектора на скаляр.
Возвращает новый объект `Vector`, координаты которого умножены на скаляр `float`.

- `Vector.__rmul__`

```Python
def __rmul__(self, scalar: float) -> "Vector"
```

Поддерживает умножение вектора на скаляр справа.
Возвращает новый объект `Vector`, координаты которого умножены на скаляр `float`.

- `Vector.__truediv__`

```Python
def  __truediv__(self, scalar: float) -> "Vector"
```

Реализует деление вектора на скаляр.
Возвращает новый объект `Vector`, координаты которого разделены на скаляр `float`.

- `Vector.__eq__`

```Python
def  __eq__(self, other: "Vector") -> bool
```

Сравнивает два вектора (или вектор и число 0) на равенство.
Если other — целое число 0, то производится сравнение с нулевым вектором.

Возвращаемое значение:
`True`, если векторы равны по соответствующим координатам, иначе `False`.

- `Vector.__bool__`

```Python
def __bool__(self)
```

Определяет логическое значение вектора.
Возвращаемое значение:
`False`, если вектор равен нулевому $(0; 0)$, иначе `True`.