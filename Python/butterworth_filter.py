# import
from scipy import signal
from scipy.signal import butter, lfilter
import numpy as np
import librosa
import matplotlib.pyplot as plt

# def


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    y = lfilter(b, a, data)
    return y


if __name__ == "__main__":
    sample_rate = 4000
    wav, sr = librosa.load('107_2b3_Ll_mc_AKGC417L.wav', sample_rate)

    new_wav = butter_bandpass_filter(wav, 100, 2000, sample_rate*2)

    plt.plot(wav)
    plt.plot(new_wav)
    plt.show()
