# import
from os.path import join
from glob import glob
from sklearn.model_selection import train_test_split
from shutil import copy2
import numpy as np
import random
from os import makedirs, listdir

if __name__ == "__main__":
    # parameters
    dataPath = 'dataset/'
    targetPath = 'dataset/'
    testSize = 0.2
    valSize = 0.1
    randomSeed = 0
    random.seed(randomSeed)
    np.random.seed(randomSeed)

    # get the directory of dataPath
    dirs = sorted(listdir(dataPath))
    if '.DS_Store' in dirs:
        dirs.remove('.DS_Store')

    # move data
    for d in dirs:
        files = sorted(glob(join(dataPath, '{}/*.wav'.format(d))))
        train, test = train_test_split(files, test_size=testSize)
        train, val = train_test_split(train, test_size=valSize)
        trainTP = join(targetPath, 'train/{}/'.format(d))
        testTP = join(targetPath, 'test/{}/'.format(d))
        valTP = join(targetPath, 'val/{}/'.format(d))
        makedirs(trainTP, exist_ok=True)
        makedirs(testTP, exist_ok=True)
        makedirs(valTP, exist_ok=True)
        for f in train:
            print(f)
            copy2(src=f, dst=trainTP)
        for f in test:
            print(f)
            copy2(src=f, dst=testTP)
        for f in val:
            print(f)
            copy2(src=f, dst=valTP)
