# import
from os import walk, makedirs
from os.path import dirname, join
import pickle
from tqdm import tqdm
from PIL import Image

# def


def pytorch_cifar10_dataset_to_png(root):
    for dirpath, _, filenames in walk(root):
        if any(['_batch' in v for v in filenames]):
            dirpath = dirname(dirpath)
            break
    files = {
        'train': [
            'data_batch_1', 'data_batch_2', 'data_batch_3', 'data_batch_4',
            'data_batch_5'
        ],
        'test': ['test_batch']
    }
    for stage in ['train', 'test']:
        target_path = join(dirpath, 'images/{}'.format(stage))
        makedirs(target_path, exist_ok=True)
        for file in files[stage]:
            with open(join(dirpath, 'cifar-10-batches-py/{}'.format(file)),
                      'rb') as f:
                content = pickle.load(f, encoding='bytes')
            # the data dimension is (length, channels, height, width)
            data = content[b'data'].reshape(-1, 3, 32, 32)
            # convert the data dimension to (length, height, width, channels)
            data = data.transpose(0, 2, 3, 1)
            filenames = content[b'filenames']
            for idx in tqdm(range(len(data))):
                image = Image.fromarray(data[idx])
                filename = join(target_path, filenames[idx].decode('utf-8'))
                image.save(fp=filename)


if __name__ == '__main__':
    # parameters
    root = 'CIFAR10'

    #
    pytorch_cifar10_dataset_to_png(root=root)
