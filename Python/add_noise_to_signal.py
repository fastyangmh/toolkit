#import
import torchaudio
import torch
import matplotlib.pyplot as plt


#def
def add_noise_to_signal(signal, snr):
    sig_avg_watts = torch.mean(signal)
    sig_avg_db = 10 * torch.log10(sig_avg_watts)
    noise_avg_db = sig_avg_db - snr
    noise_avg_watts = 10**(noise_avg_db / 10)
    noise = torch.normal(mean=0,
                         std=torch.sqrt(noise_avg_watts),
                         size=signal.shape)
    return signal + noise


if __name__ == '__main__':
    #parameters
    filepath = '0ba018fc_nohash_0.wav'
    snr = 0

    #load waveform
    wav, sample_rate = torchaudio.load(filepath)

    #add noise
    signal_noise = add_noise_to_signal(signal=wav, snr=snr)

    #display
    plt.subplot(211)
    plt.title('signal')
    plt.plot(wav[0])
    plt.ylabel('amplitude')
    plt.subplot(212)
    plt.title('signal+noise')
    plt.plot(signal_noise[0])
    plt.ylabel('amplitude')
    plt.tight_layout()
    plt.show()

    #save signal_noise to a wav file
    torchaudio.save('signal_noise.wav', signal_noise, sample_rate)
