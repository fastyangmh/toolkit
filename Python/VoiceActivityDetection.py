import os
from scipy.io.wavfile import read
import numpy as np
import webrtcvad_vad as vad
import matplotlib.pyplot as plt

input_dir='/Users/yangmh/Desktop/data16000/'
output_dir='/Users/yangmh/Desktop/process/'
waveform_dir='/Users/yangmh/Desktop/waveform/'

if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

if not os.path.isdir(waveform_dir):
    os.mkdir(waveform_dir)

for root,dir,file in os.walk(input_dir):
    files=sorted(file)

max_len=0
waves=[]
for file in files:
    rate,wav=vad.main(os.path.join(input_dir,file),3)
    if not len(wav):
        wav=read(os.path.join(input_dir,file))[1]
    if len(wav)>max_len:
        max_len=len(wav)
    waves.append(wav)

per_number_files=1
i=0
labels=[]
for idx,wav in enumerate(waves):
    diff=max_len-len(wav)
    if diff:
        wav=np.append(wav,np.zeros(diff))
    waves[idx]=wav
    labels.append(idx//per_number_files)

    plt.plot(wav)
    i+=1
    if i//per_number_files:
        i=0
        plt.title(idx//per_number_files)
        plt.tight_layout()
        plt.savefig(os.path.join(waveform_dir,str(idx//per_number_files)+'.png'))
        plt.show()

waves=np.array(waves)
labels=np.array(labels)
np.save(os.path.join(output_dir,'X'),waves)
np.save(os.path.join(output_dir,'y'),labels)


