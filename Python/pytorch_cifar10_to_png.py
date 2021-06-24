# import
import pickle
from os.path import join
from os import makedirs
from glob import glob
import numpy as np
import matplotlib.pyplot as plt

# def


def pytorch_cifar10_to_png(data_path):
    files = sorted(glob(join(data_path, 'cifar-10-batches-py/*_batch*')))
    for file in files:
        with open(file, 'rb') as f:
            content = pickle.load(f, encoding='bytes')
        data = np.reshape(content[b'data'], (-1, 32, 32, 3), 'F')
        labels = content[b'labels']
        filenames = content[b'filenames']
        stage = 'train' if 'data_batch' in file else 'test'
        target_path = join(data_path, stage)
        makedirs(target_path, exist_ok=True)
        for idx in range(len(data)):
            plt.imsave(join(target_path, filenames[idx].decode(
                "utf-8")), arr=data[idx], format='png')


if __name__ == '__main__':
    # parameters
    data_path = '/Users/yangmh/Desktop/ImageClassification/data/CIFAR10'
    target_path = 'temp'

    #
    pytorch_cifar10_to_png(data_path=data_path)
