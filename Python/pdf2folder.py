# import
from glob import glob
from os.path import basename, join
from os import makedirs
from shutil import move

if __name__ == '__main__':
    # parameters
    data_path = 'pdf'

    # get files
    files = sorted(glob(join(data_path, '*.pdf')))

    # move file to folder
    for f in files:
        folder_path = join(data_path, basename(f)[:-4])
        makedirs(folder_path, exist_ok=True)
        move(src=f, dst=folder_path)
