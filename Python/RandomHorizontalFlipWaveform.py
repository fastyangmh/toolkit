#import
import torch
import torch.nn as nn
import torchaudio
import matplotlib.pyplot as plt


#class
class RandomHorizontalFlipWaveform(nn.Module):
    def __init__(self, p=0.5) -> None:
        super().__init__()
        self.p = p

    def forward(self, waveform):
        if torch.rand(1) < self.p:
            waveform = waveform.flip(1)
        return waveform


if __name__ == '__main__':
    #parameters
    filepath = '9a2e5b3c_nohash_1.wav'

    #load waveform
    wav, sr = torchaudio.load(filepath)

    #create transform
    transform = RandomHorizontalFlipWaveform(p=1)

    #transform waveform
    hf_wav = transform(wav)

    #display
    plt.subplot(211)
    plt.title('original waveform')
    plt.plot(wav[0])
    plt.subplot(212)
    plt.title('horizontal flip waveform')
    plt.plot(hf_wav[0])
    plt.tight_layout()
    plt.show()