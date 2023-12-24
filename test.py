import numpy as np
from scipy import optimize
import math


def get_distance(power: float):
    def func(x):
        # return power + 20 * math.log10(x)
        return power + 20.0 * math.log10(x)

    result = optimize.root(func, np.array([2]))
    return result.x[0]


def f(x):
    return 10 ** (- (x - 50) / 20)

def res(p):
    return math.sqrt(p / (4 * math.pi * 6))


print(f(18))

print(get_distance(-40))
