#import
import torchaudio
from torchvision import transforms
from typing import Optional
import torch
import matplotlib.pyplot as plt
import soundfile as sf
import torch.nn as nn


#class
class DBToAmplitude(torchaudio.transforms.AmplitudeToDB):
    def __init__(self,
                 stype: str = 'power',
                 top_db: Optional[float] = None) -> None:
        super().__init__(stype=stype, top_db=top_db)

    def forward(self, x):
        power = 1.0 if self.stype == 'power' else 0.5
        return torchaudio.functional.DB_to_amplitude(x=x,
                                                     ref=self.ref_value,
                                                     power=power)


class MelSpectrogramToWaveform(nn.Module):
    def __init__(self, n_mels, n_fft) -> None:
        super().__init__()
        self.transform = transforms.Compose([
            DBToAmplitude(),
            torchaudio.transforms.InverseMelScale(n_stft=n_fft // 2 + 1,
                                                  n_mels=n_mels,
                                                  sample_rate=sample_rate),
            torchaudio.transforms.GriffinLim(n_fft=n_fft)
        ])

    def forward(self, x):
        return self.transform(x)


if __name__ == '__main__':
    #parameters
    filepath = 'audio.wav'
    n_mels = 64
    n_fft = 1024
    hop_length = n_fft // 2

    #load audio
    waveform, sample_rate = torchaudio.load(filepath)

    #create transform_mel_spectorgram
    transform_mel_spectorgram = transforms.Compose([
        torchaudio.transforms.MelSpectrogram(sample_rate=sample_rate,
                                             n_mels=n_mels,
                                             n_fft=n_fft,
                                             hop_length=hop_length),
        torchaudio.transforms.AmplitudeToDB()
    ])

    #transform the waveform
    x = transform_mel_spectorgram(waveform)

    #copy x to x_hat
    x_hat = torch.clone(x)

    #create
    transform_waveform = MelSpectrogramToWaveform(n_mels=n_mels, n_fft=n_fft)

    #transform the x_hat
    waveform_hat = transform_waveform(x_hat)

    #display the waveform
    plt.subplot(211)
    plt.plot(waveform[0])
    plt.subplot(212)
    plt.plot(waveform_hat[0])
    plt.show()

    #save the waveform
    sf.write('real.wav', waveform[0], sample_rate)
    sf.write('fake.wav', waveform_hat[0], sample_rate)
