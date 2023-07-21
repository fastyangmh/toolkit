#import
import numpy as np
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt
import seaborn as sns


#def
def calculate_intersection(x1, x2):
    #estimate kernel density
    kde1 = gaussian_kde(x1)
    kde2 = gaussian_kde(x2)

    #generate the data
    xmin = min(x1.min(), x2.min())
    xmax = max(x1.max(), x2.max())
    dx = 0.2 * (xmax - xmin)
    xmin -= dx
    xmax += dx
    data = np.linspace(xmin, xmax, len(x1))

    #get density with data
    kde1_x = kde1(data)
    kde2_x = kde2(data)

    #calculate intersect
    idx = np.argwhere(np.diff(np.sign(kde1_x - kde2_x))).flatten()
    x, y = data[idx], kde2_x[idx]
    return x, y


if __name__ == '__main__':
    #
    normal_scores=np.load('normal_scores.npy')
    anomaly_scores=np.load('anomaly_scores.npy')

    #get intersection
    x, y = calculate_intersection(x1=normal_scores, x2=anomaly_scores)

    #plot
    sns.kdeplot(x1, label='x1')
    sns.kdeplot(x2, label='x2')
    plt.plot(x, y, 'o')
    plt.legend()
    plt.show()