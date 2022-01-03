# import
import numpy as np
import matplotlib.pyplot as plt

# def


def teager_kaiser_energy_operator(signal):
    y = [0]
    for idx in range(1, len(signal)-1):
        y.append((signal[idx]**2)-(signal[idx-1]*signal[idx+1]))
    y.append(0)
    return np.array(y)


if __name__ == '__main__':
    # parameters
    duration = 5
    sample_rate = 1000
    frequence = 2
    time = np.linspace(0, duration, sample_rate*duration)

    # generate signal
    signal = np.sin(2*np.pi*frequence*time) + \
        np.sin(2*np.pi * frequence*5*time)
    signal[1000:2000] *= 2
    signal[1500:2500] *= 5

    # calculate teager kaiser energy operator
    y = teager_kaiser_energy_operator(signal=signal)

    # plot
    plt.plot(time, signal, label='siganl')
    plt.plot(time, y, label='teager kaiser')
    plt.legend()
    plt.show()
