# import
from os import walk, makedirs
from os.path import dirname, join
from torchvision.datasets import mnist
from tqdm import tqdm
from PIL import Image

# def


def pytorch_mnist_dataset_to_png(root):
    for dirpath, _, filenames in walk(root):
        if any(['ubyte' in v for v in filenames]):
            dirpath = dirname(dirpath)
            break
    files = {
        'train': {
            'images': 'train-images-idx3-ubyte',
            'labels': 'train-labels-idx1-ubyte'
        },
        'test': {
            'images': 't10k-images-idx3-ubyte',
            'labels': 't10k-labels-idx1-ubyte'
        }
    }
    for stage in ['train', 'test']:
        target_path = join(dirpath, 'images/{}'.format(stage))
        makedirs(target_path, exist_ok=True)
        images = mnist.read_image_file(
            path=join(dirpath, 'raw/{}'.format(files[stage]['images'])))
        labels = mnist.read_label_file(
            path=join(dirpath, 'raw/{}'.format(files[stage]['labels'])))
        for idx in tqdm(range(len(images))):
            prefix = str(idx).zfill(len(str(len(images))))
            filename = '{}_{}.png'.format(prefix, labels[idx])
            filename = join(target_path, filename)
            image = Image.fromarray(images[idx].numpy())
            image.save(fp=filename)


if __name__ == '__main__':
    # parameters
    root = 'MNIST'

    # convert to png
    pytorch_mnist_dataset_to_png(root=root)
