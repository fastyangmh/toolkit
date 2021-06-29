#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  7 13:20:29 2018

@author: yangmh
"""

#import
import numpy as np
from scipy.signal import stft    #短時距傅立葉變換(short-time Fourier transform, STFT)
import matplotlib.pyplot as plt
from scipy.io.wavfile import read

#def
def draw_spectrogram(time,freq,Zxx):
    plt.figure(figsize=(10,5)) 
    plt.pcolormesh(time,freq,np.abs(Zxx),cmap='terrain')
    plt.ylim([0,3500])
    plt.colorbar()
    plt.tight_layout()
    plt.show()
    
if __name__=='__main__':
    rate,signal=read('hello.wav')
    framesize=256
    freq,time,stftMatrix = stft(signal,
                                fs=rate,
                                nperseg=framesize,
                                noverlap=0)
    draw_spectrogram(time,freq,stftMatrix)
    time=np.linspace(0,len(signal),len(signal))/rate
    plt.plot(time,signal)
    plt.tight_layout()
    plt.show()