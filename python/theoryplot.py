# This script is used for testing the relation between current
# and force. No plots created from this script will be used in
# the IA.

import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.stats import linregress

root = Path(__file__).parent.parent.resolve()
data_dir = root / 'data'
data_path = data_dir / 'image-data2.csv'

with open(data_path) as datafile:
    csv_reader = csv.reader(datafile, delimiter=',')
    rawstrings = np.array(list(csv_reader)[1:]) # remove titles
    rawstrings = np.delete(rawstrings, 0, 1)
    rawdata = rawstrings.astype(np.float64)

mass = 4.9 # g +/-0.1
wire_length = 46.1 # mm +/- 0.5
pend_length = 55.6 # mm +/- 0.5

data = [] # init
for x, sx, y, sy in rawdata:
    if x == 0:
        plus_sy = sy
        diff_y = y
    else:
        data.append([x, sx, y-diff_y, sy+plus_sy])

data = np.array(data).T
X = data[0]
DX = data[1]
Y = data[2]
DY = data[3]

dtan = lambda x : np.tan(np.radians(x))
get_dy = lambda y, dy, y2 : ((dtan(y+dy) - dtan(y-dy))/ 2 / dtan(y) + (0.1/4.9)) * y2

X2 = X#np.degrees(np.arctan(X))
DX2 = DX#[get_dx(x, dx) for x, dx in zip(X, DX)]
Y2 = mass*9.81*dtan(Y)
reg = linregress(X, Y**2)
DY2 = get_dy(Y, DY, Y2)
x = np.linspace(-360, 360, 100)

#plt.plot(X, Y**2, 'k.')
plt.plot(x, np.tan(np.radians(x)), 'b')
plt.xlim(-360, 360)
plt.ylim(-5,5)
plt.show()