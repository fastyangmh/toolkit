# import
import time
from typing import Any

import cv2
from imgcat import imgcat
from tqdm import tqdm

from toolkit.file_downloader import FileDownloader
from toolkit.terminal_viewer.src.constants import DISPLAY_WIDTH
from toolkit.terminal_viewer.src.viewers.base_viewer import BaseViewer


# class
class VideoViewer(BaseViewer):
    def _load_data(self, source: str) -> cv2.VideoCapture:
        if source.startswith("http"):
            source = FileDownloader.download_to_temp(source)

        return cv2.VideoCapture(source)

    def _get_metadata(self, data: cv2.VideoCapture) -> dict[str, Any]:
        fps = data.get(cv2.CAP_PROP_FPS)
        frame_count = int(data.get(cv2.CAP_PROP_FRAME_COUNT))

        if frame_count <= 0:
            raise ValueError("Video file has no frames or is not valid.")

        width = int(data.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(data.get(cv2.CAP_PROP_FRAME_HEIGHT))

        return {
            "fps": fps,
            "frame_count": frame_count,
            "width": width,
            "height": height,
        }

    def _display_data(
        self,
        source: str,
        data: cv2.VideoCapture,
        metadata: dict[str, Any],
        display_width: int | None = DISPLAY_WIDTH,
        start_frame: int = 0,
        **kwargs,
    ) -> None:
        print(f"Displaying video from: {source}")

        frame_interval = 1 / metadata["fps"]

        video_info = (
            f"Resolution(wxh): {metadata['width']}x{metadata['height']}, "
            f"FPS: {metadata['fps']}, Frames: {metadata['frame_count']}"
        )

        if start_frame > 0:
            data.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        pbar = tqdm(initial=start_frame, total=metadata["frame_count"])

        while data.isOpened():
            try:
                start_time = time.perf_counter()
                ret, frame = data.read()
                if not ret:
                    break

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                print(f"{video_info} frame_index: {pbar.n}")
                imgcat(frame, width=display_width, **kwargs)

                pbar.update(1)

                elapsed_time = time.perf_counter() - start_time
                sleep_time = max(0, frame_interval - elapsed_time)
                time.sleep(sleep_time)
            except KeyboardInterrupt:
                print("Video playback interrupted.")
                break

        pbar.close()
        data.release()
