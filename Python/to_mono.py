#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  7 11:08:33 2018

@author: yangmh
"""

#import
from librosa.core import to_mono
from scipy.io.wavfile import read

#def
def mono_detection(signal):
    signal=signal.astype(float)
    if len(signal.shape)== 2:
        signal = to_mono(signal.T)
        return signal
    else: 
        return signal

if __name__=='__main__':
    rate,signal=read('hide.wav')
    signal=mono_detection(signal)
    