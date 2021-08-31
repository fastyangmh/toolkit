# import
import cv2
import numpy as np
from PIL import Image
import argparse

# def


def get_roi_image(image):
    # convert to numpy array
    image_array = np.array(image)

    # denoise
    blurred = cv2.medianBlur(src=image_array, ksize=7)

    # find edge
    edge = cv2.Canny(image=blurred, threshold1=30, threshold2=150)
    edge = cv2.dilate(src=edge, kernel=np.ones(
        shape=(3, 3), dtype=np.uint8), iterations=20)

    # find maximum contour
    contours, _ = cv2.findContours(
        image=edge, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
    if len(contours):
        contours = max(contours, key=cv2.contourArea)
        (x, y, w, h) = cv2.boundingRect(contours)
        image_array = image_array[y:y+h, x:x+w]
        image_height, image_width = image_array.shape
        if image_height*image_width < 10000:
            return image
        else:
            return image_array
    else:
        return image


if __name__ == '__main__':
    # parameters
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--filepath', type=str, help='the filepath.')
    filepath = parser.parse_args().filepath
    print(filepath)

    if 'background' not in filepath:
        # load image
        image = Image.open(filepath)

        # get roi image
        image = get_roi_image(image=image)

        # save image
        image = Image.fromarray(image)
        image.save('test.png')
