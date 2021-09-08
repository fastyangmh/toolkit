# import
import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse
from datetime import datetime
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# def


def load_image(filepath):
    return cv2.imread(filename=filepath)


def get_masked_image(image):
    indices = [0, 1, 2, 5, 9, 13, 17]
    with mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5) as hands:
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        image_height, image_width, _ = image.shape
        if not results.multi_hand_landmarks:
            return None, None
        hand_landmarks = results.multi_hand_landmarks[0]
        mask = np.zeros((image_height, image_width), dtype=np.uint8)
        points = [[hand_landmarks.landmark[idx].x*image_width,
                   hand_landmarks.landmark[idx].y*image_height] for idx in indices]
        points = np.array(points, dtype=np.int32)
        pt1 = [points[:, 0].min(), points[:, 1].min()]
        pt2 = [points[:, 0].max(), points[:, 1].max()]
        cv2.rectangle(img=mask, pt1=pt1, pt2=pt2, color=1, thickness=-1)
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
    color_space = cv2.COLOR_BGR2YCrCb

    # load image
    image = load_image(filepath=filepath)

    # get masked image
    mask, masked_image = get_masked_image(image=image)

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
