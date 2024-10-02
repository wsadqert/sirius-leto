from .named_widgets import *

width = 527
height = 460

labels_h2_size = (200, 35)
labels_h2 = dict()

labels_size = (125, 25)
labels = {}

labels_units_size = (30, 25)
labels_units = dict()

labels_h2_data = [
	NamedLabelH2('settings', "Настройки модели", ( 40, 80)),
	NamedLabelH2('render',   "Отображние",       (290, 250)),
	NamedLabelH2('physics',  "Физика",           (290, 80)),
]

labels_data = [
	NamedLabel('dt',          "Шаг по времени", ( -3, 120), "Шаг симуляции. Должен быть как \nминимум на 3 порядка меньше `t_max`"),
	NamedLabel('t_max',       "Конечное время", ( -3, 150), "Максимальное время симуляции"),
	NamedLabel('l',           "Длина",          (257, 120), "Длина маятника"),
	NamedLabel('alpha_start', "Начальный угол", (257, 150), "Начальный угол отклонения маятника \nот положения равновесия"),
	NamedLabel('k',           "k",              (257, 180), "Коэффициент сопротивления воздуха"),
	NamedLabel('m',           "Масса груза",	(257, 210), "Масса груза на конце маятника"),
	NamedLabel('fps',         "fps",            (257, 290), "Количество кадров анимации в секунду"),
]

lineedits_data = [
	NamedLineEdit('dt',          (120, 120), '1e-5'),
	NamedLineEdit('t_max',       (120, 150), '2'),
	NamedLineEdit('l',           (380, 120), '9.8'),
	NamedLineEdit('alpha_start', (380, 150), '50'),
	NamedLineEdit('k',           (380, 180), '0.6'),
	NamedLineEdit('m',           (380, 210), '1'),
]

labels_units_data = [
	NamedLabelUnit('dt',          "с",    (200, 120)),
	NamedLabelUnit('t_max',       "с",    (200, 150)),
	NamedLabelUnit('l',           "м",    (460, 120)),
	NamedLabelUnit('alpha_start', "рад",  (460, 150)),
	NamedLabelUnit('k',           "в ед. СИ", (460, 180)),
	NamedLabelUnit('m',           "кг",   (460, 210)),
]
labels_units_places = {
	"с ": (200, 120),
	"с": (200, 150),
	"м": (460, 120),
	"°": (460, 150),
	"кг/с": (460, 180),
	"кг": (460, 210),
}

lineedits_size = (75, 25)
lineedit_variables = dict()
lineedits = dict()

checkboxes_info = {
	"theory": ("Расчитывать аналитическое решение", (40, 190)),
	"windage": ("Учитывать сопротивление воздуха", (40, 220)),
	"extremums": ("Отображать пики на графике", (280, 355)),
	"plot_animation": ("Показать анимацию движения", (280, 385)),
	"plot_alpha": ("Показать график угла от времени", (280, 415)),
}
checkboxes_size = (230, 30)
checkbox_variables = dict()
checkboxes = dict()

radios_info = {
	"linear": ("kv", (40, 300)),
	"quadratic": ("kv^2", (130, 300))
}
radio_hints = {
	"linear": "Линейная зависимость силы \nсопротивления от скорости",
	"quadratic": "Квадратичная зависимость силы \nсопротивления от скорости",
}
radios_size = (100, 25)
radios = dict()

button_place = (30, 355)
button_size = (192, 80)
