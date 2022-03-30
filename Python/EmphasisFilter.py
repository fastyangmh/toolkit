#import
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchaudio
import matplotlib.pyplot as plt


#class
class EmphasisFilter(nn.Module):
    def __init__(self, p=0.5, lower=-0.5, upper=0.5) -> None:
        super().__init__()
        self.p = p
        self.lower = lower
        self.upper = upper

    def forward(self, waveform):
        if torch.rand(1) < self.p:
            alpha = (self.lower - self.upper) * torch.rand(1) + self.upper
            alpha = alpha.view(1, 1, -1)
            waveform = F.pad(waveform, (1, 0), 'reflect')
            waveform = F.conv1d(waveform[None], alpha)
        return waveform[0]


if __name__ == '__main__':
    #parameters
    filepath = '9a2e5b3c_nohash_1.wav'

    #load waveform
    wav, sr = torchaudio.load(filepath)

    #create transform
    transform = EmphasisFilter(p=1, lower=0, upper=0.25)

    #transform waveform
    emphasis_wav = transform(wav)

    #display
    plt.subplot(211)
    plt.title('original waveform')
    plt.plot(wav[0])
    plt.subplot(212)
    plt.title('emphasised waveform')
    plt.plot(emphasis_wav[0])
    plt.tight_layout()
    plt.show()