"""
Line of Best Fit Library
"""

# author: Julian Joaquin <j.joaquin@sjasd.ca>
#
# version: 1.3.5
#
# To be used in conjunction with numpy and matplotlib
# This is still in early implementation, the full module
# Is not working at this moment.

import numpy as np
from typing import Callable, SupportsFloat
from numpy.typing import ArrayLike
from matplotlib.axes import Axes

class LinearRegression:
    """Linear regression."""
    def __init__(self) -> None:
        self._coef = None
        self._intercept = None

    def __repr__(self) -> str:
        return f'{self.__class__}()'

    def __str__(self) -> str:
        return self.__repr__()

    @property
    def coef(self) -> float:
        return self._coef

    @property
    def intercept(self) -> float:
        return self._intercept

    def predict(self, x: SupportsFloat) -> float:
        """Predicts using the linear regression."""
        return self._coef*x + self._intercept

    def fit(self, x: ArrayLike, y: ArrayLike):
        """
        Initializer method for the linear regression.

        Parameters
        ----------
        x : ArrayLike
            the set of values for the x axis.

        y : ArrayLike
            the set of values for the y axis.

        Notes
        -----
        This function must be called with the initialization of the
        class. Specifically, call `LinearRegression().fit(x,y)`
        when initializing.
        """
        if len(x) != len(y):
            raise ValueError(
                'given sets do not have the same number of elements.'
            )
        # TODO: Compute with R value
        s_xy = len(x)*sum([a*b for a,b in zip(x,y)]) - sum(x)*sum(y)
        s_x2 = len(x)*sum([a**2 for a in x]) - (sum(x)**2)

        self._coef = s_xy / s_x2
        self._intercept = np.mean(y) - np.mean(x)*self._coef
        return self



class LinearRegressionNoInt(LinearRegression):
    """Linear regression with an intercept forced to the origin."""
    def __init__(self) -> None:
        super().__init__()

    def __repr__(self) -> str:
        return super().__repr__()

    def __str__(self) -> str:
        return super().__str__()

    @property
    def coef(self) -> float:
        return super().coef

    def predict(self, value: SupportsFloat) -> float:
        """Predicts using the linear regression."""
        return self._coef*value

    def fit(self, x: ArrayLike, y: ArrayLike):
        """
        Initializer method for the linear regression.

        Parameters
        ----------
        x : ArrayLike
            the set of values for the x axis.

        y : ArrayLike
            the set of values for the y axis.

        Notes
        -----
        This function must be called with the initialization of the
        class. Specifically, call `LinearRegressionNoInt().fit(x,y)`
        when initializing.
        
        The `_intercept` attribute is still given to this regression
        for debugging and precision purposes.
        """
        if len(x) != len(y):
            raise ValueError(
                'given sets do not have the same number of elements.'
            )
        # TODO: Compute with R value in mind
        s_xy = sum([a*b for a,b in zip(x,y)])
        s_x2 = sum([a**2 for a in x])

        self._coef = s_xy / s_x2
        self._intercept = np.mean(y) - np.mean(x)*self._coef
        return self



def hplot(ax: Axes, data1: ArrayLike, data2: ArrayLike, param_dict):
    """
    A helper function to create a matplotlib plot.

    Parameters
    ----------
    ax : Axes
        The axes to draw to

    data1 : array
        The x data

    data2 : array
        The y data

    param_dict : dict
        Dictionary of keyword arguments to pass to ax.plot

    Returns
    -------
    out : List
        list of artists (graphs) added
    """
    out = ax.plot(data1, data2, **param_dict)
    return out


def transform_linear(
        transform: Callable[[float], float], coef: float, inter: float):
    """
    Transforms a linear relation using the given function.

    Parameters
    ----------
    transform : Callable
        function or callable to transform the linear relation.

    coef : float
        the coefficient of the linear relation.

    inter : float
        the intercept of the linear relation.

    Returns
    -------
    func : Callable
        the new function transformed by the given transformation
        function

    Notes
    -----
    if *f(x)* is the transforming function, *a* is the coefficient of
    the linear relation, and *b* is the intercept, this function
    outputs:

        f(ax + b)

    This is literally implemented as:
    ```
    func = lambda x : transform(coef*x + inter)
    ```
    """
    func = lambda x : transform(coef*x + inter)
    return func


def minrange(X: ArrayLike, Xerr: ArrayLike):
    """
    Produces an array that has the minimum possible range for the
    given dataset `X` and its random error `Xerr`.

    Parameters
    ----------
    X : ArrayLike
        the main sorted dataset.

    Xerr : Arraylike
        the dispersion of the main set, or the uncertainty of each
        value in the main dataset.

    Returns
    -------
    X_new : Array
        the new set with the minimum variance possible given the
        random error.

    Notes
    -----
    The formula for this function is very primitive and should not be
    used for precise analysis. The array is produced by adding the
    dispersion `Xerr` to the respective element `X` if the index of `X`
    is less than the median index, and subtracting the dispersion if
    the index is greater than the median index.
    """
    med = np.median(X)
    X_new = np.array([
        xi+xe if xi<med else
        xi-xe if xi>med else
        xi
        for xi,xe in zip(X, Xerr)
    ])
    return X_new


def maxrange(X: ArrayLike, Xerr: ArrayLike):
    """
    Produces an array that has the maximum possible range for the
    given dataset `X` and its random error `Xerr`.

    Parameters
    ----------
    X : ArrayLike
        the main sorted dataset.

    Xerr : ArrayLike
        the dispersion of the main set, or the uncertainty of each
        value in the main dataset.

    Returns
    -------
    X_new : Array
        the new set with the minimum variance possible given the
        random error.

    Notes
    -----
    The formula for this function is very primitive and should not be
    used for precise analysis. The array is produced by substracting the
    dispersion `Xerr` to the respective element `X` if the index of `X`
    is less than the median index, and adding the dispersion if the
    index is greater than the median index.
    """
    med = np.median(X)
    X_new = np.array([
        xi-xe if xi<med else
        xi+xe if xi>med else
        xi
        for xi,xe in zip(X, Xerr)
    ])
    return X_new


def main():
    pass


if __name__ == '__main__':
    main()
