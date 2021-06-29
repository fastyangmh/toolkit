#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  8 20:47:27 2018

@author: yangmh
"""

#import
import numpy as np
from scipy.io.wavfile import read
import sys
sys.path.append('/Volumes/GoogleDrive/我的雲端硬碟/Code/Python/Speech')
from scipy.signal import stft    #短時距傅立葉變換(short-time Fourier transform, STFT)
from draw_spectrogram import draw_spectrogram

#def
def normoalization(freqbin,Zxx):
    #if freq <=250Hz or freq >=3750Hz that would be removed.  
    freqcut =  np.ones((Zxx.shape[0],1))
    for idx,element in enumerate(freqbin):
        if element <= 250 or element>=3500:
            freqcut[idx] = 0
    Zxx = Zxx * freqcut
    Zxx = np.abs(Zxx)**2
    summation =np.sum(Zxx,axis=0)
    for idx , ele in enumerate(summation):
        if ele == 0 or ele == np.nan:
            summation[idx] = 1
    Zxx = Zxx/summation
    return Zxx

if __name__=='__main__':
    rate,siganl=read('hello.wav')
    freq,time,stftMatrix=stft(siganl,fs=rate,nperseg=256,noverlap=0)
    draw_spectrogram(time,freq,stftMatrix)
    stftMatrix_nor=normoalization(freq,stftMatrix)
    draw_spectrogram(time,freq,stftMatrix_nor)
    