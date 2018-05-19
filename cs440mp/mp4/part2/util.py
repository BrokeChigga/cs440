import numpy as np
import pickle
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.ticker import FuncFormatter

def save_obj(obj, name):
    with open(name, 'wb+') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)

def output_stat(bound_list, winrate_list = []):
    fig1 = plt.figure(figsize=(10,6))
    ax = fig1.gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    x = np.arange(1, len(bound_list) + 1)
    z = np.polyfit(x, bound_list, 1)
    p = np.poly1d(z)
    plt.plot(x, bound_list)
    plt.plot(x, p(x), 'r--')
    plt.xlabel('Round', fontsize = 14)
    plt.ylabel('Bounce Count', fontsize = 14)
    plt.xlim(xmin = 1, xmax = len(bound_list))
    plt.ylim(ymin = 0)
    plt.grid(True)
    plt.title('Bounce Count Curve', fontsize = 16)

    if len(winrate_list) > 0:
        fig2 = plt.figure(figsize=(10,6))
        ax = fig2.gca()
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y))) 
        x = np.arange(1, len(winrate_list) + 1) * 5000
        plt.plot(x, winrate_list)
        plt.xlabel('Round', fontsize = 14)
        plt.ylabel('Winning Rate', fontsize = 14)
        plt.xlim(xmin = np.min(x), xmax = np.max(x))
        plt.ylim(ymin = 0, ymax = 1)
        plt.grid(True)
        plt.title('Winning Rate Curve', fontsize = 16)
    
    plt.show()