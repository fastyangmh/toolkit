# import
from PIL import Image
import matplotlib.pyplot as plt

# def


def pil_loader(path: str, in_chans) -> Image.Image:
    # open path as file to avoid ResourceWarning (https://github.com/python-pillow/Pillow/issues/835)
    with open(path, 'rb') as f:
        img = Image.open(f)
        mode = 'L' if in_chans == 1 else 'RGB'
        return img.convert(mode)


if __name__ == '__main__':
    # parameters
    filepath = 'image.png'
    in_chans = 1

    # load
    image = pil_loader(path=filepath, in_chans=in_chans)

    # display
    cmap = 'gray' if in_chans == 1 else None
    plt.imshow(image, cmap=cmap)
    plt.show()
