"""
Advanced Statistics Modelling Library
"""

# author: Julian Joaquin <j.joaquin@sjasd.ca>
#
# version: 0.0.2
#
# To be used in conjunction with numpy and matplotlib

import ibstat.core as core
import numpy as np
from numpy.typing import ArrayLike

def rmoutlier(x: ArrayLike) -> ArrayLike:
    q1, q3 = np.percentile(x, [25, 75])
    iqr = q3 - q1
    out = 1.5*iqr

    # IQR may not exist, resulting in an empty output.
    # To prevent this, should the percentiles return a zero value,
    # It will be handled as if the percentiles are negligible.
    outlier_test = lambda x : x<(q1-out) or x>(q3+out)
    if iqr == 0 or out == 0:
        #print('RMO: NO QUARTILES')
        return x
    else:
        x_new = np.array([xi for xi in x if not outlier_test(xi)])
        #print(f'RMO: SUCCESS\n\t{x=}\n\t{x_new=}')
        return x_new
