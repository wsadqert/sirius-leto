from cmath import sin, cos, sqrt, exp

from src.general.constants import *
from src.lab1_pendulum.constants import *


def phi_beta_positive(t: float):
	return alpha_start/2 * ((1 + gamma/sqrt(beta)) * exp((-gamma + sqrt(beta)) * t) + (1 - gamma/sqrt(beta)) * exp((-gamma - sqrt(beta)) * t))


def phi_beta_negative_zero(t: float):
	return alpha_start * exp(-gamma * t) * (cos(sqrt(-beta)*t) + gamma/sqrt(-beta) * sin(sqrt(-beta)*t))


used_phi_def = phi_beta_positive if beta > 0 else phi_beta_negative_zero

t_array = np.linspace(0, 5, 5000)
phi_array = [used_phi_def(i).real for i in t_array]

plt.grid(True, ls='--')
plt.xlabel('Time, s')
plt.ylabel('Angle, rad')

plt.plot(t_array, phi_array)
plt.show()
