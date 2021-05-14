# import
import torch
import torchaudio
import numpy as np
from tqdm import tqdm


# def
def time_stretch(filepath):
    wav, sample_rate = torchaudio.load(filepath)
    index = sorted(np.random.randint(0, len(wav[0]), 2))
    wav_part1 = wav[:, :index[0]]
    wav_part2 = wav[:, index[0]:index[1]]
    wav_part3 = wav[:, index[1]:]
    effect_factor_part2 = np.random.choice(
        [0, 1])  # 1 is elogation, 0 is compression
    effect_factor_part2 += np.random.rand()
    effect_factor_part1 = 2-effect_factor_part2
    effect_part1 = [['stretch', '{}'.format(effect_factor_part1)]]
    effect_part2 = [['stretch', '{}'.format(effect_factor_part2)]]
    new_wav = []
    for v, e in zip([wav_part1, wav_part2, wav_part3], [effect_part1, effect_part2, effect_part1]):
        temp = torchaudio.sox_effects.apply_effects_tensor(
            tensor=v, sample_rate=sample_rate, effects=e)[0]
        new_wav.append(temp)
    return torch.cat(new_wav, 1)


if __name__ == '__main__':
    #
    filepath = 'demo.wav'

    for idx in tqdm(range(100)):
        new_wav = time_stretch(filepath=filepath)
        torchaudio.save('temp/new_wav{}.wav'.format(idx), new_wav, 16000)
