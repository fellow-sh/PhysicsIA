# This is a modified script from 'christian' on scipython.com
# https://scipython.com/blog/visualizing-a-vector-field-with-matplotlib/

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

def E(q, r0, x, y):
    """Return the electric field vector E=(Ex,Ey) due to charge q at r0."""
    den = np.hypot(x-r0[0], y-r0[1])**3
    return q * (x - r0[0]) / den, q * (y - r0[1]) / den

# Grid of x, y points
nx, ny = 64, 64
x = np.linspace(-2, 2, nx)
y = np.linspace(-2, 2, ny)
X, Y = np.meshgrid(x, y)

charges = [
    (1, (-1, 0)), (-1, (1,0))
]

# Electric field vector, E=(Ex, Ey), as separate components
Ex, Ey = np.zeros((ny, nx)), np.zeros((ny, nx))
for charge in charges:
    ex, ey = E(*charge, x=X, y=Y)
    Ex += ex
    Ey += ey

fig = plt.figure(figsize=(4,4))
ax = fig.add_subplot(111)

# Add filled circles for the charges themselves
charge_colors = {True: '#aa0000', False: '#0000aa'}
for q, pos in charges:
    ax.add_artist(Circle(pos, 0.05, color=charge_colors[q>0]))

ax.streamplot(x, y, Ex, Ey, arrowstyle='->', arrowsize=1.5, zorder=1)

#ax.add_artist(Rectangle((-1, -0.33), 1, 0.66, color='red', zorder=2))
#ax.add_artist(Rectangle((0, -0.33), 1, 0.66, color='blue', zorder=2))

#ax.text(-0.66, 0, 'N', color='white', size=14, weight='bold',
#        ha='center', va='center')
#ax.text(0.66, 0, 'S', color='white', size=14, weight='bold',
#        ha='center', va='center')

ax.set_xlim(-2,2)
ax.set_ylim(-2,2)
ax.set_aspect('equal')
plt.axis('off')
plt.show()