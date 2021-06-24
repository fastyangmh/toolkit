# import
from os.path import join, basename
from os import makedirs, walk
import torch
import matplotlib.pyplot as plt

# def


def pytorch_mnist_to_png(data_path):
    for dirpath, _, files in walk(data_path):
        if len(list(filter(lambda x: '.pt' in x, files))) > 0:
            break
    for f in files:
        stage = 'train' if 'train' in basename(f) else 'test'
        target_path = join(data_path, 'MNIST/images/{}'.format(stage))
        makedirs(target_path, exist_ok=True)
        data, label = torch.load(join(dirpath, f))
        num_data = len(data)
        for idx in range(num_data):
            plt.imsave(join(target_path, '{}_{}.png'.format(str(idx).zfill(
                len(str(num_data))), label[idx])), arr=data[idx], cmap='gray', format='png')Ｆ


if __name__ == '__main__':
    # parameters
    data_path = 'MNIST'

    #
    pytorch_mnist_to_png(data_path=data_path)
