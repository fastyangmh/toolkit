#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 16:48:21 2018

@author: yangmh
"""

import numpy as np
from scipy.io.wavfile import read

def FrameMatrix(signal,framesize,overlap):
    strided=framesize-overlap
    frame=[]
    
    if (len(signal)-framesize)%strided != 0:
        addzerocount=strided-((len(signal)-overlap)%strided)
        signal=np.append(signal,np.zeros(addzerocount))
    
    for i in range(0,len(signal)-overlap,strided):
        temp=[]
        for j in range(framesize):
            temp.append(signal[i+j])
        frame.append(temp)
    frame=np.array(frame).T
    
    return frame

if __name__=='__main__':
    rate,signal=read('/Users/yangmh/Desktop/hello.wav')
    framesize=512
    overlap=256
    frame=FrameMatrix(signal,framesize,overlap)
    
    



