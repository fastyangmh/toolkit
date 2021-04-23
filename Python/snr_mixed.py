# import
from scipy.io.wavfile import read, write
import numpy as np
from os.path import join, basename
from glob import glob
from os import listdir, makedirs
from tqdm import tqdm

# def


def padZero(y, wavLength):
    diff = wavLength-len(y)
    padWidth = (np.floor(diff/2).astype(int), np.ceil(diff/2).astype(int))
    y = np.pad(array=y, pad_width=padWidth,
               mode='constant', constant_values=(0, 0))
    return y


def random_shift(y):
    n = len(y)
    y = np.roll(a=y, shift=np.random.randint(low=-0.5*n, high=0.5*n+1))
    return y


def read_wav(filePath, wavLength, shift=False):
    _, y = read(filename=filePath)
    if len(y) < wavLength:
        y = padZero(y=y, wavLength=wavLength)
    else:
        y = y[:wavLength]
    if shift:
        y = random_shift(y=y)
    return y


def write_wav(filePath, sr, y):
    write(filename=filePath, rate=sr, data=y)


def calculate_snr(y1, y2):
    return 20*np.log10(np.linalg.norm(y1)/np.linalg.norm(y2))


def mix_wav(y1, y2, snr):
    y2 = y2/np.linalg.norm(y2)*np.linalg.norm(y1)/(10.0**(0.05*snr))
    mixed = y1+y2
    return mixed


if __name__ == "__main__":
    # parameters
    srcPathClean = './dataset'
    srcPathNoisy = './noise'
    desPath = './15'
    sr = 8000
    wavLength = sr*5
    snr_list = [15]
    indices = []

    # get directories and files
    dirsClean = sorted(listdir(path=srcPathClean))
    noisyFiles = sorted(glob(join(srcPathNoisy, '*.wav')))

    # mix the wav and write the clean and mixed wav
    for d in tqdm(dirsClean):
        cleanFiles = sorted(glob(join(srcPathClean, '{}/*.wav'.format(d))))
        makedirs(join(desPath, d), exist_ok=True)
        for cleanFile in cleanFiles:
            yClean = read_wav(filePath=cleanFile,
                              wavLength=wavLength, shift=False)
            for snr in snr_list:
                if snr == None:
                    mixed = yClean
                    fileName = basename(cleanFile)
                else:
                    noisyIndex = np.random.permutation(len(noisyFiles))[0]
                    indices.append(noisyIndex)
                    yNoisy = read_wav(
                        filePath=noisyFiles[noisyIndex], wavLength=wavLength, shift=True)
                    mixed = mix_wav(y1=yClean, y2=yNoisy,
                                    snr=snr).astype(np.int16)
                    fileName = basename(cleanFile)[
                        :-4]+'_snr{:02}_{}.wav'.format(snr, basename(noisyFiles[noisyIndex])[:-4])
                write_wav(filePath=join(
                    desPath, '{}/{}'.format(d, fileName)), sr=sr, y=mixed)
