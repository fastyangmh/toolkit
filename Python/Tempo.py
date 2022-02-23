#import
import torchaudio
import torch.nn as nn
import torch
import matplotlib.pyplot as plt


#class
class Tempo(nn.Module):
    def __init__(self, p, factors, sample_rate) -> None:
        super().__init__()
        assert all(
            [v > 0 for v in factors]
        ), f'please set elements greater than 0 in factors.\nfactors: {factors}'
        self.p = p
        self.a = sorted(factors)[0]
        self.b = sorted(factors)[1]
        self.sample_rate = sample_rate
        self.effects = ['tempo']

    def forward(self, x):
        if torch.rand(1).item() < self.p:
            factor = (self.b - self.a) * torch.rand(1) + self.a
            effects = self.effects + [f'{factor.item()}']
            x, _ = torchaudio.sox_effects.apply_effects_tensor(
                tensor=x, sample_rate=self.sample_rate, effects=[effects])
        return x


if __name__ == '__main__':
    #parameters
    filepath = 'dog.wav'
    p = 0.5
    factors = [0.5, 1]

    #load waveofrm
    wav, sample_rate = torchaudio.load(filepath)

    #create transform
    transform = Tempo(p=p, factors=factors, sample_rate=sample_rate)

    #transform the wav
    transformed_wav = transform(wav)

    #display the dimension
    print(f'original wav: {wav.shape}')
    print(f'transformed wav: {transformed_wav.shape}')

    #plot waveform
    plt.subplot(211)
    plt.title('original wav')
    plt.plot(wav[0])
    plt.subplot(212)
    plt.title('transformed wav')
    plt.plot(transformed_wav[0])
    plt.show()