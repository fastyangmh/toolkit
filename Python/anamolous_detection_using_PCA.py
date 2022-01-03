# import
from glob import glob
from os.path import join
from PIL import Image
import numpy as np
from sklearn.decomposition import PCA, KernelPCA
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # parameters
    data_path = '/Users/yangmh/Desktop/ImageClassification/data/MNIST/MNIST/images'
    n_components = 100

    # get normal training data, let 0 as normal iamge
    train_set = []
    for f in glob(join(data_path, 'train/*_0.png')):
        train_set.append(np.array(Image.open(f).convert('L')))
    train_set = np.array(train_set).reshape(-1, 28*28).astype(float)/255.

    # get normal test data, let 0 as normal iamge
    test_set_normal = []
    for f in glob(join(data_path, 'test/*_0.png')):
        test_set_normal.append(np.array(Image.open(f).convert('L')))
    test_set_normal = np.array(
        test_set_normal).reshape(-1, 28*28).astype(float)/255.

    # get abnormal test data, let 1 as abnormal iamge
    test_set_abnormal = []
    for f in glob(join(data_path, 'test/*_1.png')):
        test_set_abnormal.append(np.array(Image.open(f).convert('L')))
    test_set_abnormal = np.array(
        test_set_abnormal).reshape(-1, 28*28).astype(float)/255.

    # train pca
    #pca = PCA(n_components=n_components).fit(train_set)
    pca = KernelPCA(n_components=n_components, n_jobs=-1,
                    fit_inverse_transform=True).fit(train_set)

    # transform train and test set
    train_set_pca = pca.transform(train_set)
    test_set_normal_pca = pca.transform(test_set_normal)
    test_set_abnormal_pca = pca.transform(test_set_abnormal)

    # inverse train and test set
    train_set_hat = pca.inverse_transform(train_set_pca)
    test_set_normal_hat = pca.inverse_transform(test_set_normal_pca)
    test_set_abnormal_hat = pca.inverse_transform(test_set_abnormal_pca)

    # plot the pca result
    plt.plot(train_set_pca[0], color='blue',
             label='normal image in training set')
    for v in train_set_pca[1:]:
        plt.plot(v, color='blue')

    plt.plot(test_set_normal_pca[0], color='green',
             label='normal image in test set')
    for v in test_set_normal_pca[1:]:
        plt.plot(v, color='green')

    plt.plot(test_set_abnormal_pca[0], color='red',
             label='abnormal image in test set')
    for v in test_set_abnormal_pca[1:]:
        plt.plot(v, color='red')

    plt.legend()
    plt.savefig('result.png')
    plt.close()

    # check inverse result
    plt.subplot(331)
    plt.title('original normal image in training set')
    plt.imshow(train_set[0].reshape(28, 28), 'gray')
    plt.subplot(332)
    plt.title('inversed normal image in training set')
    plt.imshow(train_set_hat[0].reshape(28, 28), 'gray')
    plt.subplot(333)
    plt.title(
        'difference between original and inversed normal image in training set')
    plt.imshow(train_set[0].reshape(28, 28) -
               train_set_hat[0].reshape(28, 28), 'gray')
    plt.subplot(334)
    plt.title('original normal image in test set')
    plt.imshow(test_set_normal[0].reshape(28, 28), 'gray')
    plt.subplot(335)
    plt.title('inversed normal image in test set')
    plt.imshow(test_set_normal_hat[0].reshape(28, 28), 'gray')
    plt.subplot(336)
    plt.title('difference between original and inversed normal image in test set')
    plt.imshow(test_set_normal[0].reshape(28, 28) -
               test_set_normal_hat[0].reshape(28, 28), 'gray')
    plt.subplot(337)
    plt.title('original abnormal image in test set')
    plt.imshow(test_set_abnormal[0].reshape(28, 28), 'gray')
    plt.subplot(338)
    plt.title('inversed abnormal image in test set')
    plt.imshow(test_set_abnormal_hat[0].reshape(28, 28), 'gray')
    plt.subplot(339)
    plt.title('difference between original and inversed abnormal image in test set')
    plt.imshow(test_set_abnormal[0].reshape(
        28, 28)-test_set_abnormal_hat[0].reshape(28, 28), 'gray')
    plt.show()
