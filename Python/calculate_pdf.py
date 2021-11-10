# import
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats.kde import gaussian_kde

# def


def calculate_pdf(x, normalization):
    # create Gaussian kernels
    kde = gaussian_kde(x)

    # create space
    #space = np.linspace(x.min(), x.max(), len(x))
    space = np.linspace(-x.max(), x.max(), len(x)*2)

    # calculate distribution
    dist = kde(space)
    if normalization:
        #dist = (dist-dist.min())/(dist.max()-dist.min())
        #TODO has a bug
        pass

    return space, dist


if __name__ == '__main__':
    # parameters
    n_samples = 5000
    mean = 0
    std = 1

    # generate samples
    x = np.random.normal(loc=mean, scale=std, size=(n_samples,))

    # get space and distribution
    space, dist = calculate_pdf(x=x, normalization=True)

    #plot and display
    plt.plot(space, dist)
    plt.show()
