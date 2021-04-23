# import
from argparse import Namespace
from os import listdir, makedirs
from os.path import join
from sklearn.model_selection import train_test_split
from datetime import datetime
from shutil import copytree
from glob import glob

# def


def create_dataset(projectParams):
    stageList = ['train', 'val', 'test']
    dataset = {stage: {} for stage in stageList}
    for dType in dataType:
        samples = sorted(
            glob(join(projectParams.dataPath, '{}/*/'.format(dType))))
        trainSet, valSet = train_test_split(
            samples, test_size=projectParams.valSize)
        trainSet, testSet = train_test_split(
            trainSet, test_size=projectParams.testSize)
        dataset['train'][dType] = trainSet
        dataset['val'][dType] = valSet
        dataset['test'][dType] = testSet
        for v in trainSet:
            dst = join(targetPath, '{}/{}/'.format('train', dType))
            makedirs(name=dst, exist_ok=True)
            copytree(src=v, dst=dst, dirs_exist_ok=True)
        for v in valSet:
            dst = join(targetPath, '{}/{}/'.format('val', dType))
            makedirs(name=dst, exist_ok=True)
            copytree(src=v, dst=dst, dirs_exist_ok=True)
        for v in testSet:
            dst = join(targetPath, '{}/{}/'.format('test', dType))
            makedirs(name=dst, exist_ok=True)
            copytree(src=v, dst=dst, dirs_exist_ok=True)
    return dataset


if __name__ == '__main__':
    # parameters
    projectParams = Namespace(**{'dataPath': 'fiberglass_net/',
                                 'valSize': 0.1,
                                 'testSize': 0.3,
                                 'targetPath': 'temp',
                                 'taskeName': datetime.now().strftime('%Y%m%d%H%M%S')})
    dataType = [v for v in listdir(projectParams.dataPath) if v != '.DS_Store']
    targetPath = join(projectParams.targetPath, projectParams.taskeName)

    # create train, val, test data and copy it to targetPath
    dataset = create_dataset(projectParams=projectParams)
