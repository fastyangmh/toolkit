# import
from os.path import join, realpath
from glob import glob

if __name__ == '__main__':
    # parameters
    data_path = './'

    # get files and write to txt
    for stage in ['train', 'val', 'test']:
        files = sorted(glob(join(data_path, '{}/*.png'.format(stage))))

        with open('{}.txt'.format(stage), 'w') as f:
            for file in files:
                f.write('{}\n'.format(realpath(file)))
