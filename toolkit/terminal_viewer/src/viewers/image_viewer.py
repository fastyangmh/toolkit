# import
from typing import Any

from imgcat import imgcat
from PIL import Image
from PIL.Image import Image as PILImage

from toolkit.file_downloader import FileDownloader
from toolkit.terminal_viewer.src.constants import DISPLAY_WIDTH
from toolkit.terminal_viewer.src.viewers.base_viewer import BaseViewer


# class
class ImageViewer(BaseViewer):
    def _load_data(self, source: str) -> PILImage:
        if source.startswith("http"):
            source = FileDownloader.download_to_temp(source)

        return Image.open(source)

    def _get_metadata(self, data: PILImage) -> dict[str, Any]:
        width, height = data.size

        return {"width": width, "height": height}

    def _display_data(
        self,
        source: str,
        data: Any,
        metadata: dict[str, Any],
        display_width: int | None = DISPLAY_WIDTH,
        **kwargs,
    ) -> None:
        print(f"Displaying image from: {source}")
        print(f"Image size: {metadata['width']}x{metadata['height']}")
        imgcat(data, width=display_width, **kwargs)
