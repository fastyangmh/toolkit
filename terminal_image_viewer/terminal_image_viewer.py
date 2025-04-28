# import
import argparse
import os
import tempfile

import requests
from imgcat import imgcat
from PIL import Image
from PIL.ImageFile import ImageFile
from tqdm import tqdm

# constants
TIMEOUT = 30
CHUNK_SIZE = 1024
DISPLAY_WIDTH = 60


# class
class FileDownloader:
    @classmethod
    def download_to_temp(cls, url: str) -> str:
        response = requests.get(url, stream=True, timeout=TIMEOUT)

        if not response.ok:
            raise ValueError(
                f"Failed to download file from {url} with status code {response.status_code}"
            )

        temp_dir = tempfile.mkdtemp(dir="/tmp")
        filename = os.path.basename(url)
        filepath = os.path.join(temp_dir, filename)

        print(f"Downloading file to {filepath}")

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


class TerminalImageViewer:
    def _load_image(self, source: str) -> ImageFile:
        image = Image.open(source)

        return image

    def _extract_image_metadata(self, image: ImageFile) -> tuple[int, int]:
        width = image.width
        height = image.height

        return width, height

    def play(self, source: str, display_width: int = DISPLAY_WIDTH) -> None:
        image = self._load_image(source)

        width, height = self._extract_image_metadata(image)
        image_info = f"Resolution(wxh): {width}x{height}"
        print(image_info)
        imgcat(image, width=display_width)


# def
def parse_args():
    parser = argparse.ArgumentParser(
        description="Terminal image viewer using imgcat.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "source",
        type=str,
        help="Image source like URL or file path.",
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
        args.source = FileDownloader.download_to_temp(args.source)

    player = TerminalImageViewer()
    player.play(args.source, args.display_width)


if __name__ == "__main__":
    main()
