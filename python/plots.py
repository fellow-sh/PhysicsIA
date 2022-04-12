from pathlib import Path
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np
import csv

path = Path(__file__).parent.parent.resolve() / 'data' / 'image-data.csv'

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

res1 = linregress(X, Y**3)
res2 = linregress(X, Y**2)
res3 = linregress(np.log(X), Y)
print(res1.rvalue)
print(res2.rvalue)
print(res3.rvalue)

x = np.linspace(0, 1.75, 100)
x3 = np.linspace(-2, np.log(1.75), 100)

fig, ax = plt.subplots(1, 3)

ax[0].plot(data[0], data[2]**3, 'b.')
ax[0].plot(x, res1.slope * x + res1.intercept)
ax[1].plot(data[0], data[2]**2, 'r.')
ax[1].plot(x, res2.slope * x + res2.intercept)
ax[2].plot(np.log(data[0]), data[2], '.')
ax[2].plot(x3, res3.slope * x3 + res3.intercept)
#plt.xlim(left=0, right=1.6)
#plt.ylim(bottom=0, top=20)
plt.show()
