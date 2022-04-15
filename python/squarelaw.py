# This program is a quick demonstration of the inverse square law
# through the numerical integration of an object falling towards
# Earth from a significant height.
#
# This demonstration is intended to show how this calculation and
# computation is what results in the inverse square law and indicate
# that, for this experiment, it is not dependent on this phenomenon.

from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import numpy as np

G = 6.67408e-11 # kg^-1 m^2
m1 = 5.9722e24 # kg sun


def eq(t, X):
    x, xdot = X[0], X[1]
    xddot = - G*m1 / (x**2)
    return np.array([xdot, xddot])

sol = solve_ivp(eq, [0, 5e6], [6.371e6 + 1e9, 0], atol=1e-12, rtol=3e-14)
plt.plot(sol.t, sol.y[0,...])
plt.show()
