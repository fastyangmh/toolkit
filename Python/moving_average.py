#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 09:27:20 2018

@author: yangmh
"""

def MovingAverage(S,K):
    Signal=np.copy(S)
    temp=0
    for k in range(len(Signal)):
        a=-K+k
        b=K+k+1
        if a<0:
            a=0
        if b>len(Signal):
            b=len(Signal)
        for i in range(a,b):
            temp+=S[i]
        temp/=(2*K)+1
        Signal[k]=temp
        temp=0
    return Signal

def frameMat(signal,frame , overlap ):
    step = frame - overlap
    Signalsize = np.size(signal)
     # note: Signalsize和overlap都是int 型別所以必須轉型，另外ceil return float
     #或者使用 frameCount = np.ceil(( float(Signalsize - frame)/ step) ) +1  # method 2
    frameCount = np.ceil(float(Signalsize - overlap)/step)
    # create frameSize * frameCount matrix
    enframe  =  np.zeros((frame,int(frameCount )))

    #知道frameSize ,overlap ,signalSize ,以補零的方式 將signalSize的長度補為可以被frame整除
    if (Signalsize-frame) % step != 0:
        addZeroCount =step-((Signalsize -overlap )%step)
        for i in range(1 ,addZeroCount+1,1 ):
            signal=np.insert(signal,Signalsize,0,axis = 0)

    #依據frameSize ,overlap,來將signal排至每個行向量    
    for i in range(0, int(frameCount),1):
        if i == 0 :
            enframe [ :, i ] = signal[0 : frame]
            point = frame 
        else:
            start = point -overlap
            enframe [ : , i ] = signal[ start : start + frame  ]
            point = start + frame 
        
    return enframe

#import
from scipy.io.wavfile import read,write
import matplotlib.pyplot as plt
import numpy as np

#compute
framesize=512
overlap=256
rate,signalOrigin=read('鐘聲&聖經_小聲原始.wav')
enframeOrigin=frameMat(signalOrigin,framesize,overlap)
rows,cols=enframeOrigin.shape
volumearray=np.zeros(cols)
for i in range(cols):
    frame=enframeOrigin[:,i]-np.mean(enframeOrigin[:,i])
    volumearray[i]=sum(np.abs(frame))    
frametime =  (np.linspace( 0,cols, cols)*(framesize-overlap)) /rate
sampletime=(np.linspace(1,len(signalOrigin),len(signalOrigin)))/rate
volumearrayMovingAverage=MovingAverage(volumearray,32)

#plot result
plt.subplot(311)
plt.title('Origin Signal')
plt.plot(sampletime,signalOrigin)
plt.subplot(312)
plt.title('Energy')
plt.plot(frametime,volumearray)
plt.subplot(313)
plt.title('Moving Average Energy')
plt.plot(frametime,volumearrayMovingAverage)
plt.tight_layout()
plt.show()















