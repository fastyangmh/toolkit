# import
from glob import glob
from os.path import join, basename, dirname
from argparse import Namespace
import librosa
from tqdm import tqdm
from librosa.display import specshow
import matplotlib.pyplot as plt
import numpy as np

# def


def wav_to_image_feature(parameters, file):
    y = librosa.load(path=file, sr=parameters.sampleRate)[0]
    S = librosa.feature.melspectrogram(y=y, sr=parameters.sampleRate)
    return librosa.power_to_db(S, ref=np.max)


if __name__ == '__main__':
    # parameters
    parameters = Namespace(**{'dataPath': 'SpokenDigitDataset',
                              'sampleRate': 16000})

    #
    for stage in ['train', 'val', 'test']:
        print(stage)
        files = glob(join(parameters.dataPath, '{}/*/*.wav'.format(stage)))
        for file in tqdm(files):
            feature = wav_to_image_feature(parameters=parameters, file=file)
            specshow(feature, x_axis='time', y_axis='mel')
            plt.axis('off')
            plt.savefig(join(dirname(file), basename(file)[
                        :-3]+'png'), bbox_inches='tight', pad_inches=0)
            plt.close()
