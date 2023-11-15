<script
  src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript">
</script>

# Лаборатория №1. Физический маятник.
ID: `lab1_pendulum`

<span style="color:yellow">PyCharm не умеет корректно обрабатывать нотацию LaTex, даже с подключённым скриптом от [mathjax.org](https://mathjax.org), лучше просматривать этот файл с помощью VS Code или аналогичного редактора. Ну или напрямую на GitHub.</span>

## Описание лаборатории

Согласно [определению](https://ru.wikipedia.org/wiki/Физический_маятник) с Википедии,
> Физический маятник — осциллятор, представляющий собой твёрдое тело, совершающее колебания в поле каких-либо сил относительно точки, не являющейся центром масс этого тела, или неподвижной оси, перпендикулярной направлению действия сил и не проходящей через центр масс этого тела.


## Входные данные

### Константы:
- $l$ - длина маятника (м),
- $\alpha_0$ - начальный угол отклонения маятника (рад),
- $k_{windage}$ - коэффициент сопротивления воздуха,
- $m$ - масса тела.

### Независимые переменные:
- $t$ - время.

### Зависимые переменные:
- $\alpha$ - угол отклонения маятинка от положения равновесия (рад). 

## Математика

$$
\begin{align*} 
  \gamma &= \frac{k}{2m}, \\ 
  \beta &= \gamma^2 - \frac{g}{l} = \frac{k^2}{4m^2} - \frac{g}{l},\\
  k &= k_{windage}'\cdot\mathrm{d}t,\\
  c_1 &= \gamma\cdot \mathrm d t = \frac{\mathrm dt\cdot k}{2m},\\
  c_2 &= \frac{g\cdot \mathrm dt^2}{l}.
\end{align*}
$$

### 1. Численное решение

#### a) Линейная зависимость силы сопротивления от скорости

$$\alpha_{i+1} = \frac{4\alpha_i - \alpha_{i-1}(2-k) - 2c_2\sin{\alpha_i}}{2+k}$$

#### b) Квадратичная зависимсть

$$\alpha_{i+1} = 2\alpha_i - \alpha_{i-1} - 2c_1(\alpha_i-\alpha_{i-1}) - c_2\sin{\alpha_i}$$

### 2. Аналитическое решение (в приближении малых углов)
Только линеная зависимость.

#### a) $\beta>0$

$$\alpha_i(t) = \mathfrak{Re}\left(\frac{\alpha_0}{2}\cdot \left[\left\{1+\frac{\gamma}{\sqrt \beta}\right\} \cdot \exp \left(\left\{-\gamma + \sqrt \beta \right\} t\right) + \left\{1-\frac{\gamma}{\sqrt \beta}\right\}\cdot \exp \left(\left\{-\gamma - \sqrt \beta \right\} t\right) \right]\right)$$

#### b) $\beta\le0$

$$\alpha_i(t) = \mathfrak{Re}\left(\alpha_0\cdot \exp(-\gamma t)\cdot \frac{\gamma + \cos\left(t\sqrt{-\beta}\right)}{\sqrt{-\beta}}\cdot \sin\left(t\sqrt{-\beta}\right)\right)$$

Считается, что все вычисления производятся в комплексном множестве.
## Получаемые данные

- $\alpha (t)$,
- $x(t), y(t)$ - декартовы координаты центра качания.

## Полезные ссылки

- https://ru.wikipedia.org/wiki/Физический_маятник
- ...
