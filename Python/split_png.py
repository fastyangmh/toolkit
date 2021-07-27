# import
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from tqdm import tqdm
import pytesseract

if __name__ == '__main__':
    # parameters
    filepath = 'test.png'
    target_path = 'temp'

    # load image
    image = Image.open(filepath).convert('L')
    image = np.array(image)
    height, width = image.shape

    # get each font
    fonts = []
    for row in range(0, height, 150):
        for col in range(0, width, 150):
            fonts.append(Image.fromarray(image[row:row+150, col:col+150]))

    # save to target
    for idx, v in tqdm(enumerate(fonts)):
        v.save('{}/{}.png'.format(target_path, idx), dpi=(300, 300))