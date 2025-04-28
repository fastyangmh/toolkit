# import
import argparse
import os
import tempfile
import time

import cv2
import requests
from imgcat import imgcat
from tqdm import tqdm

# constants
TIMEOUT = 30
CHUNK_SIZE = 1024
DISPLAY_WIDTH = 60


# class
class FileDonwloader:
    @classmethod
    def download_to_temp(cls, url: str) -> str:
        response = requests.get(url, stream=True, timeout=TIMEOUT)

        if not response.ok:
            raise ValueError(
                f"Failed to download video from {url} with status code {response.status_code}"
            )

        temp_dir = tempfile.mkdtemp(dir="/tmp")
        filename = os.path.basename(url)
        filepath = os.path.join(temp_dir, filename)

        print(f"Downloading video to {filepath}")

        with open(filepath, "wb") as file:
            for chunk in tqdm(
                response.iter_content(CHUNK_SIZE),
                desc="Downloading",
                leave=True,
                unit="B",
            ):
                if chunk:
                    file.write(chunk)

        return filepath


class TerminalVideoPlayer:
    def _open_video_capture(self, source: str) -> cv2.VideoCapture:
        if source.isdigit():
            source = int(source)  # type: ignore

        capture = cv2.VideoCapture(source)

        if not capture.isOpened():
            raise ValueError(f"Unable to open video source: {source}")

        return capture

    def _extract_video_metadata(
        self, capture: cv2.VideoCapture
    ) -> tuple[float, float, int, int, int]:
        fps = capture.get(cv2.CAP_PROP_FPS)
        frame_interval = 1 / fps if fps > 0 else 0
        frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        return fps, frame_interval, frame_count, width, height

    def play(
        self,
        source: str,
        start_frame: int = 0,
        display_width: int = DISPLAY_WIDTH,
    ) -> None:
        capture = self._open_video_capture(source)
        capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        fps, frame_interval, frame_count, width, height = self._extract_video_metadata(
            capture
        )
        video_info = (
            f"Resolution(wxh): {width}x{height}, FPS: {fps}, Frames: {frame_count}"
        )

        pbar = tqdm(initial=start_frame, total=frame_count)

        while capture.isOpened():
            try:
                start_time = time.perf_counter()
                ret, frame = capture.read()
                if not ret:
                    break

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                print(f"{video_info} frame_index: {pbar.n}")
                imgcat(frame, width=display_width)

                pbar.update(1)

                elapsed_time = time.perf_counter() - start_time
                sleep_time = max(0, frame_interval - elapsed_time)
                time.sleep(sleep_time)
            except KeyboardInterrupt:
                print("Video playback interrupted.")
                break

        pbar.close()
        capture.release()


# def
def parse_args():
    parser = argparse.ArgumentParser(
        description="Terminal video player using imgcat.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "source",
        type=str,
        help="Video source like URL, RTSP, camera index, or file path.",
    )
    parser.add_argument(
        "--start-frame",
        type=int,
        default=0,
        help="Start playing from this frame index.",
    )
    parser.add_argument(
        "--display-width",
        type=int,
        default=DISPLAY_WIDTH,
        help="Display width in terminal.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    print(args)

    if args.source.startswith("http"):
        args.source = FileDonwloader.download_to_temp(args.source)

    player = TerminalVideoPlayer()
    player.play(
        args.source,
        args.start_frame,
        args.display_width,
    )


if __name__ == "__main__":
    main()
