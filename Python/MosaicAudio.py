# import
import numpy as np
from copy import copy
import random
import torch
import torchaudio
import torch.nn.functional as F
from typing import List, AnyStr

# def


def pad_waveform(waveform, max_waveform_length):
    diff = max_waveform_length-len(waveform)
    pad = (int(np.ceil(diff/2)), int(np.floor(diff/2)))
    waveform = F.pad(input=waveform, pad=pad)
    return waveform

# class


class MosaicAudio:
    def __init__(self, sample_rate, target_waveform_length, original_filepath, mix_filepaths):
        self.sample_rate = sample_rate
        self.target_waveform_length = int(
            sample_rate*(target_waveform_length/(len(mix_filepaths)+1)))
        self.original_filepath = original_filepath
        self.mix_filepaths = mix_filepaths

    def _vad(self, filepath):
        wav, sample_rate = torchaudio.load(filepath)
        threshold = torch.abs(wav).mean()
        voiced_index = torch.where(wav > threshold)[1]
        wav = wav[:, voiced_index[0]:voiced_index[-1]
                  ][:, :self.target_waveform_length]
        if len(wav[0]) < self.target_waveform_length:
            wav = pad_waveform(
                waveform=wav, max_waveform_length=self.target_waveform_length)
        assert sample_rate == self.sample_rate, 'the sample_rate does not the same.'
        return wav

    def __call__(self):
        wav = []
        for filepath in [self.original_filepath]+self.mix_filepaths:
            wav.append(self._vad(filepath=filepath))
        return torch.cat(wav, 1)


if __name__ == '__main__':
    # parameters
    original_filepath = 'temp/train_00001.wav'
    mix_filepaths = ['temp/train_00004.wav',
                     'temp/train_00005.wav',
                     'temp/train_00007.wav',
                     'temp/train_00010.wav',
                     'temp/train_00012.wav']
    sample_rate = 8000
    target_waveform_length = 5

    # create objective
    obj = MosaicAudio(sample_rate=sample_rate, target_waveform_length=target_waveform_length,
                      original_filepath=original_filepath, mix_filepaths=mix_filepaths)

    # run
    new_wav = obj()

    # save waveform
    torchaudio.save('test.wav', new_wav, sample_rate)
