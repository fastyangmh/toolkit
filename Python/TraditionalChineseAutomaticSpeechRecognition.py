# import
import pyaudio
from typing import Any
import numpy as np
from tqdm import tqdm
import soundfile as sf
from transformers import (
    Wav2Vec2ForCTC,
    Wav2Vec2Processor,
    AutoTokenizer,
    AutoModelWithLMHead
)
from time import sleep
import torch

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
        print('Will start recording in 3 seconds')
        sleep(3)
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


class ASRModel:
    def __init__(self, model_name, sample_rate) -> None:
        self.model = Wav2Vec2ForCTC.from_pretrained(
            model_name)
        self.processor = Wav2Vec2Processor.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(
            "ckiplab/gpt2-base-chinese")
        self.gpt_model = AutoModelWithLMHead.from_pretrained(
            "ckiplab/gpt2-base-chinese")
        self.sample_rate = sample_rate

    def __call__(self, frames):
        features = self.processor(frames, sampling_rate=self.sample_rate, padding=True, return_tensors="pt")
        input_values = features.input_values
        attention_mask = features.attention_mask
        with torch.no_grad():
            logits = self.model(
                input_values, attention_mask=attention_mask).logits

        decoded_results = []
        for logit in logits:
            pred_ids = torch.argmax(logit, dim=-1)
            mask = pred_ids.ge(1).unsqueeze(-1).expand(logit.size())
            vocab_size = logit.size()[-1]
            voice_prob = torch.nn.functional.softmax(
                (torch.masked_select(logit, mask).view(-1, vocab_size)), dim=-1)
            gpt_input = torch.cat(
                (torch.tensor([self.tokenizer.cls_token_id]), pred_ids[pred_ids > 0]), 0)
            gpt_prob = torch.nn.functional.softmax(self.gpt_model(
                gpt_input).logits, dim=-1)[:voice_prob.size()[0], :]
            comb_pred_ids = torch.argmax(gpt_prob*voice_prob, dim=-1)
            decoded_results.append(self.processor.decode(comb_pred_ids))

        return decoded_results


if __name__ == '__main__':
    # parameters
    channels = 1
    sample_rate = 16000
    chunk = 1024
    record_seconds = 5
    model_name = 'voidful/wav2vec2-large-xlsr-53-tw-gpt'

    # create object
    obj = GetSound(channels=channels, sample_rate=sample_rate, chunk=chunk)

    # get sound
    frames = obj(record_seconds=record_seconds, output_filename='wave.wav')

    # convert frames to float
    frames = frames/np.iinfo(frames.dtype).max

    # create ASR model
    model = ASRModel(model_name=model_name, sample_rate=sample_rate)

    # recognition the sound
    transcription = model(frames=frames)

    # display the reuslt
    print(transcription)
