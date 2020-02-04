import matplotlib.pyplot as plt
import numpy as np


def function(x, min):
    if x < min:
        return 0
    elif x > 1 - min:
        return 1
    else:
        min_min = min
        return ((x) - min_min) * (1 + (2 * min))


def function_t(x, scale):
    return (np.tanh((x - 0.5) * scale) + 1) / 2


def plot_fun():
    og_values = np.arange(-1, 3, 0.001)
    y = [function_t(x, 1) for x in og_values]
    plt.plot(og_values, y)
    plt.show()

if __name__ == '__main__':
    plot_fun()
