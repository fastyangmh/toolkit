#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  9 11:12:12 2018

@author: yangmh
"""

#import
import numpy as np
from scipy.io.wavfile import read
import sys
sys.path.append('/Volumes/GoogleDrive/我的雲端硬碟/Code/Python/Speech')
from frameMat import frameMat

#def
def CompuEntropy(x):
    adder = 0 
    for element in x :
        if element != 0:
            adder = adder+(element*np.log2(element))
    return adder

def EntropyArr(Zxx):
    frameSize , frameCount  = Zxx.shape
    entArr = np.zeros(frameCount)
    for i in range(frameCount):
        entArr[i] = CompuEntropy(Zxx[:,i])         
    return entArr

if __name__=='__main__':
    rate,signal=read('hello.wav')
    frameMatrix=frameMat(signal,256,128)
    entropy=EntropyArr(frameMatrix)