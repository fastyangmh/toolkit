#import
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchaudio
import matplotlib.pyplot as plt


#class
class RandomShuffleWaveform(nn.Module):
    def __init__(self, sample_rate, seconds, p=0.5) -> None:
        super().__init__()
        self.p = p
        self.step = int(sample_rate * seconds)

    def forward(self, waveform):
        if torch.rand(1) < self.p:
            channels, length = waveform.shape
            frames = [
                waveform[:, idx:idx + self.step]
                for idx in range(0, length, self.step)
            ]
            indices = torch.randperm(n=len(frames)).tolist()
            frames = [frames[idx] for idx in indices]
            waveform = torch.cat(frames, -1)
        return waveform


if __name__ == '__main__':
    #parameters
    filepath = '9a2e5b3c_nohash_1.wav'

    #load waveform
    wav, sr = torchaudio.load(filepath)

    #create transform
    transform = RandomShuffleWaveform(sample_rate=16000, seconds=0.1, p=1)

    #transform waveform
    shuffled_wav = transform(wav)

    #display
    plt.subplot(211)
    plt.title('original waveform')
    plt.plot(wav[0])
    plt.subplot(212)
    plt.title('shuffled waveform')
    plt.plot(shuffled_wav[0])
    plt.tight_layout()
    plt.show()