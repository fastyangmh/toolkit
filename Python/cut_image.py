# import
import cv2
import numpy as np
from glob import glob
from os.path import join, basename

# def


def cut_image(filename):
    # load image
    # the image channel order is BGR
    img = cv2.imread(filename=filename)

    # preprocess
    blurred = cv2.medianBlur(src=img, ksize=11)

    # find edge
    gray = cv2.cvtColor(src=blurred, code=cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edge = cv2.Canny(image=blurred, threshold1=30, threshold2=150)
    kernel = np.ones(shape=(3, 3), dtype=np.uint8)
    edge = cv2.dilate(src=edge, kernel=kernel, iterations=30)

    # contours
    contours, _ = cv2.findContours(
        image=edge, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)

    # calculate the rectangle from the center
    contours = max(contours, key=cv2.contourArea)
    (x, y, w, h) = cv2.boundingRect(contours)

    # get the rectangle from the img
    img = img[y:y+h, x:x+w]

    return img


if __name__ == '__main__':
    # parameters
    dataPath = 'fiberglass_net_2class/'
    targetPath = 'temp'

    # get files
    files = glob(join(dataPath, '*/*/*.png'))

    for f in files:
        img = cut_image(filename=f)
        cv2.imwrite(filename=join(targetPath, basename(f)), img=img)
