# import
import cv2
import numpy as np
from glob import glob
from os.path import join, basename, dirname
from os import makedirs
from tqdm import tqdm

# def


def get_xyxy_from_image(filepath):
    # load image
    img = cv2.imread(filename=filepath)

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
    x1, y1, x2, y2 = x, y, x+w, y+h

    return img, x1, y1, x2, y2


def xyxy_to_xywh(x1, y1, x2, y2, img_w, img_h):
    x_center = ((x1+x2)/2)/img_w
    y_center = ((y1+y2)/2)/img_h
    yolo_w = (x2-x1)/img_w
    yolo_h = (y2-y1)/img_h
    return x_center, y_center, yolo_w, yolo_h


if __name__ == '__main__':
    # parameters
    data_path = 'fiberglass_net_GUI_light_3class'
    target_path = 'temp'
    makedirs(target_path, exist_ok=True)

    # get classes
    classes = [basename(v) for v in sorted(glob(join(data_path, 'train/*')))]
    class_to_idx = {k: idx for idx, k in enumerate(classes)}

    # write classes to classes.txt
    with open(join(target_path, 'classes.txt'), 'w') as f:
        for c in classes:
            f.write('{}\n'.format(c))

    #
    for stage in ['train', 'val', 'test']:
        # create directory
        makedirs(join(target_path, stage), exist_ok=True)

        # get files
        files = sorted(glob(join(data_path, '{}/*/*.png'.format(stage))))

        for idx, filepath in enumerate(tqdm(files)):
            # get xyxy
            img, x1, y1, x2, y2 = get_xyxy_from_image(filepath=filepath)

            # get xywh
            img_h, img_w, _ = img.shape
            x_center, y_center, yolo_w, yolo_h = xyxy_to_xywh(
                x1=x1, y1=y1, x2=x2, y2=y2, img_w=img_w, img_h=img_h)

            # save image
            filename = '{}_{}'.format(
                str(idx+1).zfill(5), basename(dirname(filepath)))
            cv2.imwrite(
                join(target_path, '{}/{}.png'.format(stage, filename)), img)

            # save annotations
            with open(join(target_path, '{}/{}.txt'.format(stage, filename)), 'w') as f:
                f.write('{} {} {} {} {}'.format(
                    class_to_idx[basename(dirname(filepath))], x_center, y_center, yolo_w, yolo_h))
