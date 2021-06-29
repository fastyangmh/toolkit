import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt
from  scipy.io.wavfile import read,write
import os

def butter_lowpass(cutoff, fs, order=20):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return np.int16(y)

if __name__=='__main__':    
    order = 5
    fs = 16000       # sample rate, Hz
    cutoff = 3000  # desired cutoff frequency of the filter, Hz
    
    input_dir='/Users/yangmh/Desktop/wav/'
    output_dir='/Users/yangmh/Desktop/lowpass/'

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    for root,dir,file in os.walk(input_dir):
        files=sorted(file)
    
    for file in files:
        rate,wav=read(os.path.join(input_dir,file))
        wav=butter_lowpass_filter(wav,cutoff,fs=rate,order=order)
        write(os.path.join(output_dir,file),rate,wav)

