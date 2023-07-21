#import
from PIL import Image
import torch.nn.functional as F
import numpy as np
import torch.nn as nn
import torchvision


#class
class ResizePadding(nn.Module):
    def __init__(self,
                 target_size: int,
                 interpolation=torchvision.transforms.functional.
                 InterpolationMode.BILINEAR,
                 max_size=None,
                 antialias=None) -> None:
        super().__init__()
        self.target_size = target_size
        self.interpolation = interpolation
        self.max_size = max_size
        self.antialias = antialias

    def forward(self, img):
        w, h = img.size  #img is PIL image
        ratio = min(self.target_size / w, self.target_size / h)
        target_w, target_h = int(w * ratio), int(h * ratio)
        img = torchvision.transforms.functional.resize(
            img=img,
            size=(target_h, target_w),
            interpolation=self.interpolation,
            max_size=self.max_size,
            antialias=self.antialias)
        img = torchvision.transforms.functional.to_tensor(
            img)  #convert PIL image to tensor
        diff_w = self.target_size - target_w
        diff_h = self.target_size - target_h
        pad = (int(np.ceil(diff_w / 2)), int(np.floor(diff_w / 2)),
               int(np.ceil(diff_h / 2)), int(np.floor(diff_h / 2)))
        img = F.pad(input=img, pad=pad)
        return torchvision.transforms.functional.to_pil_image(
            pic=img, mode=None)  #convert tensor to PIL image


if __name__ == '__main__':
    #parameters
    filepath = 'image.png'

    #load image
    image = Image.open(fp=filepath)

    #create transfrom
    transform = ResizePadding(target_size=224)

    #transform the image
    image_transformed = transform(image)

    #display
    print(image)
    print(image_transformed)
    image.show()
    image_transformed.show()