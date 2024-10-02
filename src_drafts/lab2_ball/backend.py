import matplotlib.pyplot as plt
from typing import Final

import numpy as np
from scipy.constants import g
from tqdm import tqdm
import bisect

sqrt = lambda x: x**(1/2)

h0: Final[float] = 2
v0: Final[float] = 5
q = 0.9

dt = 1e-5

c0 = sqrt(q)
c1 = (sqrt(2*g*h0 + v0**2) - v0) / g
c2 = 2/g * (sqrt(2*g*h0) + v0) * c0 / (1 - c0)

print(c1)
print(c2)


def get_time(n: int):
	assert isinstance(n, int)

	return c1 + c2 * (1 - c0 ** n)


def get_ans():
	return c1 + c2


t_falls = []
h = []
for i in range(100):
	t_falls.append(get_time(i))

print(t_falls)

t_max = get_ans()

t = list(np.arange(0, t_falls[0], dt)) + list(np.arange(t_falls[0], t_max, dt))

for i in tqdm(np.arange(0, t_falls[0], dt)):
	h.append(h0 - v0*i - g*i**2 / 2)

jmp_cnt = 0

for i in np.arange(t_falls[0], t_max, dt):
	jump_count = bisect.bisect_right(t_falls, i)
	v_i = (v0 + sqrt(2*g*h0)) * sqrt(q)**jump_count

	y = v_i * (i - t_falls[jump_count - 1]) - g/2 * (i - t_falls[jump_count - 1])**2

	h.append(y)

	if jump_count != jmp_cnt:
		jmp_cnt = jump_count
		print(jmp_cnt, i, t_falls[jump_count - 1])

plt.grid(True, ls='--')
plt.plot(t, h)
plt.plot(t_falls, [0] * len(t_falls), linestyle='', marker='o')
plt.plot([get_ans()], [0], linestyle='', marker='o')

plt.show()
