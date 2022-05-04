import numpy as np
import matplotlib
import scipy.interpolate
import torch

from numpy.polynomial.polynomial import Polynomial
from matplotlib import pyplot as plt
from torch import optim
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.cluster import KMeans
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import plot_tree


matplotlib.rcParams.update({'axes.grid' : True})
# matplotlib.rcParams['figure.figsize'] = [12, 8]
matplotlib.rcParams['figure.dpi'] = 160


def random_points(size: int = 10):
    x = np.linspace(0, 1, size)
    y = np.sin(x*10) + x * 3 + np.random.randn(size) * 0.3
    return np.stack([x, y])


def f(x, params):
    return sum(
       k * x**i
       for i, k in enumerate(params)
    )


def lagrange(x, y):
    poly = scipy.interpolate.lagrange(x, y)
    # looks too weird https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.lagrange.html
    return Polynomial(poly.coef[::-1]).coef


def cluster(mean, sigma=np.identity(2), count=100):
   return np.random.randn(count, 2) @ sigma + mean


def plot_decision_boundary(model, X, Y, h=0.02, margin=1, cmap='Paired_r'):
    x_min, x_max = X[:,0].min() - margin, X[:,0].max() + margin
    y_min, y_max = X[:,1].min() - margin, X[:,1].max() + margin
    xx, yy = np.meshgrid(
        np.arange(x_min, x_max, h), np.arange(y_min, y_max, h)
    )
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    plt.contourf(xx, yy, Z, cmap=cmap, alpha=0.55)
    plt.contour(xx, yy, Z, colors='k', linewidths=0.7)
    plt.scatter(X[:,0], X[:,1], c=Y, cmap=cmap, edgecolors='k');
