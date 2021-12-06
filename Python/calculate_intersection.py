#import
import numpy as np
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt
import seaborn as sns


#def
def calculate_intersection(x1, x2):
    #estimate kernel density
    kde1 = gaussian_kde(x1)  #, bw_method=0.5)
    kde2 = gaussian_kde(x2)  #, bw_method=0.5)

    #generate the data
    xmin = min(x1.min(), x2.min())
    xmax = max(x1.max(), x2.max())
    dx = 0.2 * (xmax - xmin)
    xmin -= dx
    xmax += dx
    data = np.linspace(xmin, xmax, size)

    #get density with data
    kde1_x = kde1(data)
    kde2_x = kde2(data)

    #calculate intersect
    idx = np.argwhere(np.diff(np.sign(kde1_x - kde2_x))).flatten()
    x, y = data[idx], kde2_x[idx]
    return x, y


if __name__ == '__main__':
    #parameters
    size = 1000

    #generate distribution
    x1 = np.abs(np.random.normal(loc=0, scale=0.3, size=size))
    x2 = np.random.rand(size)

    #get intersection
    x, y = calculate_intersection(x1=x1, x2=x2)

    #plot
    sns.kdeplot(x1, label='x1')
    sns.kdeplot(x2, label='x2')
    plt.plot(x, y, 'o')
    plt.legend()
    plt.show()