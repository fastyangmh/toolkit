# import
from glob import glob
from os import makedirs, listdir
from os.path import join
from posixpath import basename
import random
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# class


class TraditionalChineseHandwritingDataset:
    def __init__(self, filepath):
        self.filepath = filepath
        self.dirs = sorted([v for v in listdir(filepath)
                            if v != '.DS_Store'], key=int)
        self._get_character()

    def _get_character(self):
        character = {}
        for d in tqdm(self.dirs):
            char = basename(
                glob(join(self.filepath, '{}/*.png'.format(d)))[0]).split('_')[0]
            character[char] = d
        self.character = character

    def _get_image(self):
        image_path = random.sample(glob(
            join(self.filepath, '{}/*.png'.format(random.sample(self.dirs, 1)[0]))), 1)[0]
        image = np.array(Image.open(image_path))
        label = basename(image_path).split('_')[0]
        return image, label

    def __call__(self, num_of_char):
        images = []
        labels = []
        for _ in range(num_of_char):
            image, label = self._get_image()
            images.append(image)
            labels.append(label)
        return np.concatenate(images, 1), labels


if __name__ == '__main__':
    # parameters
    # please follow the https://github.com/AI-FREE-Team/Traditional-Chinese-Handwriting-Dataset
    filepath = 'cleaned_data'
    target_path = 'temp'
    number_of_files = 10000
    makedirs(target_path, exist_ok=True)

    # create object
    obj = TraditionalChineseHandwritingDataset(filepath=filepath)

    # save image
    for idx in tqdm(range(number_of_files)):
        image, labels = obj(num_of_char=random.randint(3, 4))
        plt.imshow(image)
        plt.axis('off')
        plt.savefig(join(target_path, '{}_{}.png'.format(
            idx, ''.join(labels))), bbox_inches='tight', pad_inches=0)
        plt.close()

    # save character
    with open(join(target_path, 'character.txt'), 'w') as f:
        for char in tqdm(obj.character.keys()):
            f.write('{}\n'.format(char))
