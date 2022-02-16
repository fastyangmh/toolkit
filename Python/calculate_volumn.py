#import
from posixpath import basename
import torchaudio
import torch.nn.functional as F
import torch
import numpy as np
import matplotlib.pyplot as plt


#def
def calculate_volumn(wav, win_length, hop_length):
    volumn = []
    for idx in range(0, wav.shape[-1], hop_length):
        f = wav[:, idx:idx + win_length]
        if f.shape[-1] < win_length:
            diff = win_length - f.shape[-1]
            f = F.pad(f, pad=(0, diff))
        v = 10 * torch.log10(torch.sum(torch.pow(
            f, 2))).item()  # 10*log_{10}\sum_{i=1}^n s_i^2
        volumn.append(v)
    return np.array(volumn)


def calculate_frame_time(frames, win_length, hop_length, sample_rate):
    return np.linspace(0, len(frames), len(frames)) * (
        (win_length - hop_length) / sample_rate)


if __name__ == '__main__':
    #parameters
    filepath = '00000139.wav'
    win_length = 1024
    hop_length = 512

    #load file
    wav, sample_rate = torchaudio.load(filepath)

    #calculate volumn
    volumn = calculate_volumn(wav=wav,
                              win_length=win_length,
                              hop_length=hop_length)

    #calculate frame time
    time = calculate_frame_time(frames=volumn,
                                win_length=win_length,
                                hop_length=hop_length,
                                sample_rate=sample_rate)

    #display
    plt.title(basename(filepath))
    plt.plot(time, volumn)
    plt.xlabel('Time(sec)')
    plt.ylabel('Volumn(dB)')
    plt.show()