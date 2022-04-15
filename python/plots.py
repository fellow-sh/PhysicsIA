from pathlib import Path
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np
import csv

plt.rcParams['text.usetex'] = True
plt.rcParams.update({'font.size': 11})

path = Path(__file__).parent.parent.resolve() / 'data' / 'image-data2.csv'

with open(path) as datafile:
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

f1 = plt.figure()
ax1 = f1.add_subplot(111)
ax1.errorbar(X, Y, DY, DX, '.')
ax1.set_xlabel(r'Current (\textit{A})')
ax1.set_ylabel(u'Angle (\u00b0)')
ax1.set_xlim(left=0, right=1.6)
ax1.set_ylim(bottom=0)
ax1.grid()

dtan = lambda x : np.tan(np.radians(x))
get_dy = lambda y, dy, y2 : (dtan(y+dy) - dtan(y-dy))/2 / dtan(y) * y2

X2 = X#np.degrees(np.arctan(X))
DX2 = DX#[get_dx(x, dx) for x, dx in zip(X, DX)]
Y2 = mass*9.81*dtan(Y)
DY2 = get_dy(Y, DY, Y2)

f2 = plt.figure()
ax2 = f2.add_subplot(111)
ax2.errorbar(X2, Y2, DY2, DX2, '.')

res2 = linregress(X2, Y2)
x = np.linspace(np.min(X2)*(0.8), np.max(X2)*1.1, 100)

ax2.plot(x, (res2.slope * x + res2.intercept), 'k')

ax2.set_xlabel(r'Current (A)')
ax2.set_ylabel(r'Force (mN)')
ax2.set_xlim(left=0, right=1.6)
ax2.set_ylim(bottom=0)
ax2.grid()

eqstr1 = r'$y=%.2fx + %.2f$' % (res2.slope, res2.intercept)
eqstr2 = r'$y=%.2fx %.2f$' % (res2.slope, res2.intercept)

textstr = '\n'.join((
    eqstr1 if res2.intercept >= 0 else eqstr2,
    r'$\rho=%.4f$' % (res2.rvalue, )))

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

ax2.text(0.05, 0.95, textstr, transform=ax2.transAxes, fontsize=12,
        verticalalignment='top', bbox=props)

plt.show()
