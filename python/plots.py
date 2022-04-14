from pathlib import Path
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np
import csv

path = Path(__file__).parent.parent.resolve() / 'data' / 'image-data2.csv'

with open(path) as datafile:
    csv_reader = csv.reader(datafile, delimiter=',')
    rawstrings = np.array(list(csv_reader)[1:]) # remove titles
    rawstrings = np.delete(rawstrings, 0, 1)
    rawdata = rawstrings.astype(np.float64)

data = []
for x, sx, y, sy in rawdata:
    if x == 0:
        plus_sy = sy
        diff_y = y
        continue
    else:
        data.append([x, sx, y-diff_y, sy+plus_sy])

data = np.array(data).T
X = data[0]
Y = data[2]

f1 = plt.figure()
ax1 = f1.add_subplot(111)
ax1.errorbar(X, Y, data[3], data[1], 'b.')
ax1.set_xlim(left=0)
ax1.set_ylim(bottom=0)
ax1.grid()

Y2 = 4.9 * 9.81 * np.sin(np.radians(Y))

f2 = plt.figure()
ax2 = f2.add_subplot(111)
ax2.plot(X, Y2**2, '.', color='orange')

res2 = linregress(X, Y2**2)
x = np.linspace(0, 1.75, 100)

ax2.plot(x, res2.slope * x + res2.intercept)

print(np.sqrt(res2.slope))
plt.show()
