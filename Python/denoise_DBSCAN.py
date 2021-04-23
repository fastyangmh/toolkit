# import
import librosa
from glob import glob
from os.path import join
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
from os import listdir
from shutil import copy2
import matplotlib.pyplot as plt

# def


def load_wav(file, sampleRate, maxWavLength):
    y, _ = librosa.load(file, sampleRate)
    targetLength = sampleRate*maxWavLength
    if len(y) > targetLength:
        y = y[:targetLength]
    else:
        diff = targetLength-len(y)
        padWidth = (int(np.floor(diff/2)), int(np.ceil(diff / 2)))
        y = np.pad(array=y, pad_width=padWidth,
                   mode='constant', constant_values=(0, 0))
    return y


if __name__ == '__main__':
    # parameters
    dataPath = 'testDataset'
    dataType = listdir(dataPath)
    sampleRate = 8000
    seed = 0
    targetPath = 'temp'
    min_samples = 5

    # find maxWavLength
    files = sorted(glob(join(dataPath, '*/*.wav')))
    maxWavLength = []
    for f in files:
        maxWavLength.append(librosa.get_duration(filename=f))
    maxWavLength = max(maxWavLength)

    # process
    for dType in dataType:
        if dType == '.DS_Store':
            continue
        # set seed
        np.random.seed(seed)
        # get files
        files = sorted(glob(join(join(dataPath, dType), '*.wav')))
        # get wav
        data = []
        for f in files:
            data.append(load_wav(file=f, sampleRate=sampleRate,
                                 maxWavLength=maxWavLength))
        data = np.array(data)
        # pca
        pca = PCA(n_components=2)
        dataPCA = pca.fit_transform(data)
        # dbscan
        db = DBSCAN(min_samples=min_samples)
        y = db.fit_predict(dataPCA)
        # copy
        for f in np.array(files)[y == -1]:
            copy2(f, targetPath)
        # show
        plt.title('{}'.format(dType))
        plt.scatter(dataPCA[y != -1, 0], dataPCA[y != -1, 1],
                    label='normal, totla: {}'.format(sum(y != -1)))
        plt.scatter(dataPCA[y == -1, 0], dataPCA[y == -1, 1],
                    label='abnormal, total: {}'.format(sum(y == -1)))
        plt.legend()
        plt.tight_layout()
        plt.savefig('{}.png'.format(dType))
        plt.close()
