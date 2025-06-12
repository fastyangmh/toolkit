# import
import argparse

from toolkit.file_downloader.src import FileDownloader


# def
def parse_args():
    parser = argparse.ArgumentParser(
        description="Download a file from a URL to a temporary directory.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("url", type=str, help="The URL of the file to download.")
    return parser.parse_args()


def main():
    args = parse_args()
    url: str = args.url

    file_path = FileDownloader.download_to_temp(url)
    print(f"File downloaded successfully to: {file_path}")


if __name__ == "__main__":
    main()
