# import
import argparse

import mlx.core as mx

from toolkit.automatic_speech_recognition.src import ModelFactory


# def
def parse_args():
    parser = argparse.ArgumentParser(
        description="Automatic speech recognition inference script.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--cache-limit",
        type=int,
        default=0,
        help="If using more than the given limit, "
        "free memory will be reclaimed from the cache on the next allocation. "
        "To disable the cache, set the limit to ``0``. The unit is GB.",
    )
    parser.add_argument(
        "--model-type",
        choices=tuple(ModelFactory.registry.keys()),
        type=str,
        default="ParakeetASRModel",
        help="Type of the ASR model to use.",
    )
    parser.add_argument(
        "--model-id",
        type=str,
        default="mlx-community/parakeet-tdt-0.6b-v2",
        help="Model ID for the ASR model.",
    )
    parser.add_argument(
        "--use-fp32",
        action="store_true",
        help="Use FP32 precision.",
    )
    parser.add_argument(
        "audio_files",
        type=str,
        nargs="+",
        help="Path(s) to audio file(s) for transcription (any spoken content).",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    mx.set_cache_limit(args.cache_limit * 1024**3)

    model = ModelFactory.build(
        model_type=args.model_type,
        model_info={
            "model_id": args.model_id,
            "use_fp32": args.use_fp32,
        },
    )

    outputs: list[str] = model.transcribe(inputs=args.audio_files)

    for idx, (audio_file, output) in enumerate(zip(args.audio_files, outputs)):
        print(f"Audio file {idx + 1}: {audio_file}")
        print(f"Transcription: {output}\n")


if __name__ == "__main__":
    main()
