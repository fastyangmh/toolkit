# import
import os
import tempfile

import requests
from tqdm import tqdm

from toolkit.file_downloader.src.constants import CHUNK_SIZE, TIMEOUT


# class
class FileDownloader:
    @classmethod
    def download_to_temp(cls, url: str) -> str:
        response = requests.get(url, stream=True, timeout=TIMEOUT)

        if not response.ok:
            raise ValueError(
                f"Failed to download file from {url} with status code {response.status_code}"
            )

        temp_dir = tempfile.mkdtemp()
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
