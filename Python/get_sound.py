# import
import pyaudio
import numpy as np
from argparse import Namespace
import soundfile as sf


def get_sound(parameters):
    p = pyaudio.PyAudio()
    stream = p.open(format=parameters.format, channels=parameters.channels,
                    rate=parameters.rate, input=True, output=True, frames_per_buffer=parameters.chunk)
    data = []
    time = parameters.time
    print('start record')
    while time > 0:
        time -= 1
        buffer = stream.read(parameters.chunk)
        data.append(np.frombuffer(buffer, dtype=np.float32))
    print('finish record')
    return np.concatenate(data, 0)


if __name__ == "__main__":
    # parameters
    parameters = Namespace(**{'chunk': 8000,
                              'rate': 8000,
                              'format': pyaudio.paFloat32,
                              'channels': 1,
                              'time': 5})

    # get sound
    data = get_sound(parameters=parameters)

    # save sound
    sf.write(file='sound.wav', data=data, samplerate=parameters.rate)
