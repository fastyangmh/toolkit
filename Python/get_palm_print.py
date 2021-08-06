# import
import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse
from datetime import datetime

# def


def load_image(filepath):
    return cv2.imread(filename=filepath)


def get_masked_image(image, lower, upper, color_space):
    image_color_space = cv2.cvtColor(src=image, code=color_space)
    mask = cv2.inRange(src=image_color_space, lowerb=lower, upperb=upper)
    contours, _ = cv2.findContours(
        image=mask, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image=mask, contours=contours,
                     contourIdx=-1, color=1, thickness=-1)
    mask = cv2.morphologyEx(src=mask, op=cv2.MORPH_CLOSE, kernel=np.ones(
        shape=(3, 3), dtype=np.uint8), iterations=3)
    masked_image = cv2.bitwise_and(src1=image, src2=image, mask=mask)
    masked_image = cv2.cvtColor(src=masked_image, code=cv2.COLOR_BGR2GRAY)
    return mask, masked_image


def get_palm_image(mask, masked_image):
    distance = cv2.distanceTransform(
        src=mask, distanceType=cv2.DIST_L1, maskSize=3)
    maxdist = 0
    for i in range(distance.shape[0]):
        for j in range(distance.shape[1]):
            dist = distance[i][j]
            if maxdist < dist:
                x = j
                y = i
                maxdist = dist
    half_slide = maxdist  # * np.cos(np.pi / 4)
    (left, right, top, bottom) = ((x - half_slide),
                                  (x + half_slide), (y - half_slide), (y + half_slide))
    palm_image = masked_image[int(top):int(bottom), int(left):int(right)]
    return palm_image


def get_edges(image):
    sobelX = cv2.Sobel(src=image, ddepth=cv2.CV_64F, dx=1, dy=0)
    sobelY = cv2.Sobel(src=image, ddepth=cv2.CV_64F, dx=0, dy=1)
    sobelX = np.uint8(np.abs(sobelX))
    sobelY = np.uint8(np.abs(sobelY))
    edges = cv2.bitwise_or(src1=sobelX, src2=sobelY)
    return edges


def plot_images(titles, images, cmaps, save=False):
    assert len(titles) == len(images) == len(
        cmaps), 'the input parameters does not same length.'
    n = len(titles)
    for idx in range(len(titles)):
        plt.subplot(1, n, 1+idx)
        plt.title(titles[idx])
        plt.imshow(images[idx], cmap=cmaps[idx])
    if save:
        plt.tight_layout()
        plt.savefig('{}.png'.format(datetime.now().strftime(
            '%Y%m%d%H%M%S')), bbox_inches='tight', dpi=500)
        plt.close()
    else:
        plt.show()


if __name__ == '__main__':
    # argparse
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--filepath', type=str, help='the data path.')
    parser.add_argument('--save', action='store_true',
                        default=False, help='whether to save the image.')
    parser = parser.parse_args()

    # parameters
    filepath = parser.filepath
    save = parser.save
    lower = np.array([0, 140, 0], dtype=np.uint8)
    upper = np.array([255, 200, 255], dtype=np.uint8)
    color_space = cv2.COLOR_BGR2YCrCb

    # load image
    image = load_image(filepath=filepath)

    # get masked image by ycrcb
    mask, masked_image = get_masked_image(
        image=image, lower=lower, upper=upper, color_space=color_space)

    # get palm image
    palm_image = get_palm_image(mask=mask, masked_image=masked_image)

    # get palm edge
    palm_edge = get_edges(image=palm_image)

    # plot images
    plot_images(titles=['original image', 'mask', 'masked image', 'palm image', 'palm edge'],
                images=[cv2.cvtColor(image, cv2.COLOR_BGR2RGB),
                        mask, masked_image, palm_image, palm_edge],
                cmaps=[None,  'gray', 'gray', 'gray', 'gray'],
                save=save)
