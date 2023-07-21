#import
from PIL import Image
import torch.nn.functional as F
import numpy as np
import torchvision


#class
class PaddingResize(torchvision.transforms.Resize):
    def __init__(self,
                 size,
                 interpolation=torchvision.transforms.functional.
                 InterpolationMode.BILINEAR,
                 max_size=None,
                 antialias=None):
        super().__init__(size, interpolation, max_size, antialias)

    def forward(self, img):
        w, h = img.size  #img is PIL image
        img = torchvision.transforms.functional.to_tensor(
            img)  #convert PIL image to tensor
        target_size = max(w, h)
        diff_w = target_size - w
        diff_h = target_size - h
        pad = (int(np.ceil(diff_w / 2)), int(np.floor(diff_w / 2)),
               int(np.ceil(diff_h / 2)), int(np.floor(diff_h / 2)))
        img = F.pad(input=img, pad=pad)
        img = torchvision.transforms.functional.to_pil_image(
            pic=img, mode=None)  #convert tensor to PIL image
        return super().forward(img=img)


if __name__ == '__main__':
    #parameters
    filepath = 'image.png'

    #load image
    image = Image.open(fp=filepath)

    #create transfrom
    transform = PaddingResize(size=224)

    #transform the image
    image_transformed = transform(image)

    #display
    print(image)
    print(image_transformed)
    image.show()
    image_transformed.show()