#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  9 15:50:09 2018

@author: yangmh
"""

#import
import numpy as np
from scipy.io.wavfile import read

#def
def frameMat(signal,frame,overlap):
    step = frame - overlap
    Signalsize = np.size(signal)
     # note: Signalsize和overlap都是int 型別所以必須轉型，另外ceil return float
     #或者使用 frameCount = np.ceil(( float(Signalsize - frame)/ step) ) +1  # method 2
    frameCount = np.ceil(float(Signalsize - overlap)/step)
    # create frameSize * frameCount matrix
    frameCut  =  np.zeros((frame,int(frameCount )))
    #知道frameSize ,overlap ,signalSize ,以補零的方式 將signalSize的長度補為可以被frame整除
    if (Signalsize-frame) % step != 0:
        addZeroCount =step-((Signalsize -overlap )%step)
        for i in range(1 ,addZeroCount+1,1 ):
            signal=np.insert(signal,Signalsize,0,axis = 0)
        '''    
        print signal
        print addZeroCount
        '''
    #依據frameSize ,overlap,來將signal排至每個行向量    
    for i in range(0, int(frameCount),1):
        if i == 0 : 
            frameCut [ :, i ] = signal[0 : frame]
            point = frame 
        else:
            start = point -overlap
            frameCut [ : , i ] = signal[ start : start + frame  ]
            point = start + frame 
    return frameCut

if __name__=='__main__':
    rate,signal=read('hello.wav')
    frameMatrix=frameMat(signal,256,128)
    
    
    
    
    
    
    
