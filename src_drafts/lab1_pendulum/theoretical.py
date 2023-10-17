import numpy as np
from cmath import sin, cos, sqrt, exp
from matplotlib import pyplot as plt

phi0 = 0.001
g = 9.801
l = 10

gamma = 0
beta = gamma**2 - g/l

# pre-calculate constant values
sqrt_beta = sqrt(beta)
gamma_div_sqrt_beta = gamma / sqrt_beta


def phi_beta_positive(t: float):
	return phi0/2 * ((1 + gamma_div_sqrt_beta) * exp((-gamma + sqrt_beta) * t) + (1 - gamma_div_sqrt_beta) * exp((-gamma - sqrt_beta) * t))


def phi_beta_negative_zero(t: float):
	return phi0 * exp(-gamma * t) * (cos(sqrt_beta*t) + gamma_div_sqrt_beta * sin(sqrt_beta*t))


used_phi_def = phi_beta_positive if beta > 0 else phi_beta_negative_zero

t_array = np.linspace(0, 5, 5000)
phi_array = [used_phi_def(i).real for i in t_array]

plt.grid(True, ls='--')
plt.xlabel('Time, s')
plt.ylabel('Angle, rad')

plt.plot(t_array, phi_array)
plt.show()
