# Класс `Point`

Наследуется от [`GeometryBasic`](GeometryBasic.md).

Представляет точку на плоскости.

## Аттрибуты

- `x`: float — x-координата точки
- `y`: float — y-координата точки

## Методы

- `Point.to_tuple`

```Python
def to_tuple(self) -> tuple[float, float]
```

Представляет точку как кортеж из 2 координат: `(x, y)`.

## Операторы

- `Point.__add__`

```Python
def __add__(self, other: Point | Vector) -> Point
```

Осуществляет сложение координат с переданным объектом (`Point` или [`Vector`](Vector.md)).
Возвращает новый объект `Point`.

- `Point.__sub__`

```Python
def __sub__(self, other: Point | Vector) -> Point
```

Осуществляет вычитание координат переданного объекта (`Point` или [`Vector`](Vector.md)) из координат данного.
Возвращает новый объект `Point`.

- `Point.__iadd__`

```Python
def __iadd__(self, other: Point | Vector) -> Point
```

Осуществляет сложение координат с переданным объектом (`Point` или [`Vector`](Vector.md)).
Изменяет существующий объект `Point`.

- `Point.__isub__`

```Python
def __isub__(self, other: Point | Vector) -> Point
```

Осуществляет вычитание координат переданного объекта (`Point` или [`Vector`](Vector.md)) из координат данного.
Изменяет существующий объект `Point`.

- `Point.__eq__`

```Python
def __eq__(self, other: Point) -> bool
```

Проверяет равенство координат переданного объекта `Point` с данным.
Возвращает `True` если обе координаты `x`, `y` равны, иначе `False`.
