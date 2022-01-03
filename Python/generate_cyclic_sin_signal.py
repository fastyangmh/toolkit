# import
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # parameters
    duration = 5
    sample_rate = 1000
    frequence = 2
    time = np.linspace(0, duration, sample_rate*duration)

    # generate signal
    signal = np.sin(2*np.pi*frequence*time)   # 2*π*f*t

    # display
    plt.plot(time, signal)
    plt.xlabel('time')
    plt.show()
