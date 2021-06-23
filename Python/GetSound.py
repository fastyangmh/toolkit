# import
import pyaudio
from typing import Any
import numpy as np
from tqdm import tqdm
import soundfile as sf

# class


class GetSound:
    def __init__(self, channels, sample_rate, chunk) -> None:
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=channels,
                                  rate=sample_rate,
                                  input=True,
                                  frames_per_buffer=chunk)
        self.channels = channels
        self.sample_rate = sample_rate
        self.chunk = chunk

    def __call__(self, record_seconds, output_filename=None) -> Any:
        print("* recording")
        frames = []
        for _ in tqdm(range(0, int(self.sample_rate / self.chunk * record_seconds))):
            data = self.stream.read(self.chunk, exception_on_overflow=False)
            frames.append(np.frombuffer(data, dtype=np.int16))
        frames = np.concatenate(frames, 0)
        print("* done recording")

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        if output_filename is not None:
            self.save_file(frames=frames, output_filename=output_filename)
        return frames

    def save_file(self, frames, output_filename):
        sf.write(output_filename, frames, self.sample_rate)


if __name__ == '__main__':
    # parameters
    channels = 1
    sample_rate = 16000
    chunk = 1024
    record_seconds = 5

    # create object
    obj = GetSound(channels=channels, sample_rate=sample_rate, chunk=chunk)

    # get sound
    frames = obj(record_seconds=record_seconds)

    # save sound
    obj.save_file(frames=frames, output_filename='wave.wav')
