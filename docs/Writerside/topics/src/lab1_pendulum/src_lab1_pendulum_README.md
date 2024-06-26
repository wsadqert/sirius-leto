<script
  src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript">
</script>

# Лаборатория №1. Физический маятник.
ID: `lab1_pendulum`

## Описание лаборатории

Согласно определению с [Википедии](https://ru.wikipedia.org/wiki/Физический_маятник),
> _Физический маятник_ — осциллятор, представляющий собой твёрдое тело, совершающее колебания в поле каких-либо сил относительно точки, не являющейся центром масс этого тела, или неподвижной оси, перпендикулярной направлению действия сил и не проходящей через центр масс этого тела.


## Входные данные

### Константы:
- `l` - длина маятника (м),
- `alpha_0` - начальный угол отклонения маятника (рад),
- `k` - коэффициент сопротивления воздуха (Н$\cdot $с/м),
- `m` - масса тела (кг).

### Независимые переменные:
- `t` - время (c).

### Зависимые переменные:
- `alpha` - угол отклонения маятинка от положения равновесия (рад). 

## Математика

```tex
\begin{align*} 
  \gamma &= \frac{k}{2m}, \\ 
  \beta &= \gamma^2 - \frac{g}{l} = \frac{k^2}{4m^2} - \frac{g}{l},\\
  c_1 &= \gamma\cdot \mathrm dt = \frac{\mathrm dt\cdot k}{2m},\\
  c_2 &= \frac{g\cdot \mathrm dt^2}{l}.
\end{align*}
```

### 1. Численное решение

Для удобства считается, что 
```tex
\alpha_1 = \alpha_0.
```

#### a) Линейная зависимость силы сопротивления от скорости

```tex
\alpha_{i+1} = \frac{4\alpha_i - \alpha_{i-1}(2-k) - 2c_2\sin{\alpha_i}}{2+k}
```

#### b) Квадратичная зависимсть

```tex
\alpha_{i+1} = 2\alpha_i - \alpha_{i-1} - 2c_1(\alpha_i-\alpha_{i-1}) - c_2\sin{\alpha_i}
```

### 2. Аналитическое решение (в приближении малых углов)
Только линейная зависимость.

#### a) `beta > 0`

```tex
\alpha_i(t) = \mathfrak{Re}\left(\frac{\alpha_0}{2}\cdot \left[\left\{1+\frac{\gamma}{\sqrt \beta}\right\} \cdot \exp \left(\left\{-\gamma + \sqrt \beta \right\} t\right) + \left\{1-\frac{\gamma}{\sqrt \beta}\right\}\cdot \exp \left(\left\{-\gamma - \sqrt \beta \right\} t\right) \right]\right)
```

#### b) `beta ≤ 0`

```tex
\alpha_i(t) = \mathfrak{Re}\left(\alpha_0\cdot \exp(-\gamma t)\cdot \frac{\gamma + \cos\left(t\sqrt{-\beta}\right)}{\sqrt{-\beta}}\cdot \sin\left(t\sqrt{-\beta}\right)\right)
```

Считается, что все вычисления производятся в комплексном множестве.
## Получаемые данные

- ```tex
  \alpha (t)
```
```

- ```tex
  x(t), y(t)
```
```

## Полезные ссылки

- [](https://ru.wikipedia.org/wiki/Физический_маятник)
- ...
