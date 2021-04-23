# import
import numpy as np
import scipy
import librosa
from scipy.fftpack import fft, ifft
import matplotlib.pyplot as plt

# def


def SpectralSubtraction(wav, n_frame, frame_size, overlap):
    step = frame_size-overlap
    stft = librosa.stft(wav)  # , n_fft=frame_size, hop_length=step)
    magnitude = np.abs(stft)
    phase = np.exp(1.0j * np.angle(stft))
    noise = np.mean(magnitude[:, :n_frame], axis=1).reshape(-1, 1)
    # ,hop_length=step, win_length=frame_size)
    new_wav = librosa.istft((magnitude-noise)*phase)
    return new_wav


def OnSpecSubstract(data, f_size, n_frames, bias=1):
    """
    data is the complete signal
    f_size is the size of frames
    n_frames is the number of noisy frames
    bias is used for over or under subtraction of noise
    """

    """
    samples stores a list of overlapped windows of size f_size
    phases stores the phase information of every frame
    out will be the final reconstructed signla
    """
    samples = []
    phases = []
    out = []

    lps = int(len(data)/f_size)+1

    """
    Hanning Window to apply windowing function on each frame.
    """
    hn_win = np.hanning(f_size)

    for i in range(0, (lps*2)):

        """
        Extract 50% overlapping frames of size f_size from signal and append to samples.
        """
        f_loc = int(i*f_size/2)
        samples.append(np.asarray(data[(f_loc):(f_loc+f_size)]))

        """
        Apply Hanning Windowing Function on each frame.
        DFT each frame using FFT.
        Save phase information of each frame in list phases for later use.
        Extract magnitude of each frame.
        """
        l_ele = len(samples)-1
        samples[l_ele] = samples[l_ele] * hn_win[:len(samples[l_ele])]
        samples[l_ele] = fft(samples[l_ele])
        phases.append(np.angle(samples[l_ele]))
        samples[l_ele] = abs(samples[l_ele])

        if (len(samples[l_ele]) < f_size):
            break

    """
    Assuming first frew frames are only noisy frames. Sum all the noisy frames in one
    frame.
    """
    noise = np.asarray(samples[0])
    for i in range(1, n_frames):
        noise = list(map(lambda x, y: x + y, noise, samples[i]))

    """
    Get an average noise magnitude.
    """
    noise = list(map(lambda x: x/n_frames, noise))
    noise = np.mean(noise)

    """
    Multiply bias to noise.
    """
    noise *= bias

    """
    Delete noisy frames and their respective phase information from samples and phases.
    """
    del samples[:n_frames]
    del phases[:n_frames]

    """
    Perform Spectral Subtraction
    """
    samples = [list(map(lambda x: x - noise, i)) for i in samples]

    """
    Perform Half Wave Rectification.
    """
    for idx, frm in enumerate(samples):
        samples[idx] = [0 if i < noise else i for i in frm]

    """
    Zero off negitive amplitudes.
    Multiply phase information with their respective frames.
    Perform IFFT.
    """
    for idx, data in enumerate(samples):
        samples[idx] = [0 if i < 0 else i for i in data]
        samples[idx] = list(map(lambda x, y: x*np.exp(1j*y),
                                samples[idx], phases[idx]))
        samples[idx] = ifft(samples[idx])

    """
    Overlap Add all frames.
    """
    out = samples[0]
    del samples[0]

    for data in samples:

        if len(data) == f_size:

            dm_pnt = int(f_size/2)
            om_pnt = int(len(out)-dm_pnt)

            """
            Add the overlapping parts of consecutive frames.
            """
            out[om_pnt:] = list(
                map(lambda x, y: x + y, out[om_pnt:], data[:dm_pnt]))
            out = np.concatenate([out, data[dm_pnt:]])

    return np.abs(out)


if __name__ == "__main__":
    sample_rate = 4000
    filepath = '204_2b5_Ar_mc_AKGC417L.wav'

    wav, sr = librosa.load(filepath, sample_rate)

    new_wav = SpectralSubtraction(wav, 10, 1024, 0)

    plt.subplot(211)
    plt.plot(wav)
    plt.subplot(212)
    plt.plot(new_wav)
    plt.show()
