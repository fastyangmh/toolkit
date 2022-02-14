#import
import torch
import torch.nn as nn
import torchaudio


#class
class MultiScaleMelSpectrogramLoss(nn.Module):
    def __init__(self, n_fft_list, hop_length_list, n_mels_list,
                 sample_rate) -> None:
        super().__init__()
        transforms = []
        for n_fft, hop_length, n_mels in zip(n_fft_list, hop_length_list,
                                             n_mels_list):
            transforms.append(
                torchaudio.transforms.MelSpectrogram(sample_rate=sample_rate,
                                                     n_fft=n_fft,
                                                     hop_length=hop_length,
                                                     n_mels=n_mels))
        self.transforms = transforms
        self.loss_function = nn.L1Loss()

    def forward(self, fake_waveform, real_waveform):
        loss = 0
        for transform in self.transforms:
            y_pred = transform(fake_waveform)
            y_true = transform(real_waveform)
            loss += self.loss_function(y_pred, y_true)
        return loss


if __name__ == '__main__':
    #parameters
    sample_rate = 16000
    duration = 1
    n_fft_list = [128, 256, 512, 1024]
    hop_length_list = [64, 128, 256, 512]
    n_mels_list = [16, 32, 64, 64]

    #generate waveform
    real_waveform = torch.rand(size=(1, sample_rate * duration))

    #generate fake waveform
    fake_waveform = real_waveform + torch.normal(
        mean=0, std=0.01, size=real_waveform.shape)

    #create MultiScaleMelSpectrogramLoss object
    loss_function = MultiScaleMelSpectrogramLoss(
        n_fft_list=n_fft_list,
        hop_length_list=hop_length_list,
        n_mels_list=n_mels_list,
        sample_rate=sample_rate)

    #calculate loss
    loss = loss_function(fake_waveform, real_waveform)

    #display loss
    print(loss)
