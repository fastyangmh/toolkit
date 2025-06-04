# Automatic Speech Recognition

> **Note:** This tool is designed for Apple Silicon processors (e.g., M1, M2) and may not function correctly on other architectures.

This repository offers a streamlined Automatic Speech Recognition (ASR), enabling straightforward integration and efficient inference for speech-to-text applications.

## Features

- Modular architecture supporting customizable inference pipelines
- Intuitive command-line interface for ASR operations

## Installation

This project utilizes [uv](https://github.com/astral-sh/uv) for dependency management. Please ensure `uv` is installed:

```bash
pip install uv
```

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/automatic_speech_recognition.git
cd automatic_speech_recognition
uv sync
```

## Usage

### Running ASR on an Audio File

To perform speech recognition on an audio file, execute the following script:

```bash
#!/bin/bash
python main.py speech.wav
```

## Contributing

Contributions are encouraged. To contribute, please open an issue or submit a pull request.

## License

This project is distributed under the MIT License.
