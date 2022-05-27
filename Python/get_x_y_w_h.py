#import
import cv2
import numpy as np


#def
def get_x_y_w_h(image):
    contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)

    x_center_list = []
    y_center_list = []
    yolo_w_list = []
    yolo_h_list = []
    for ct in contours:
        ct = ct[:, 0]
        x_min, y_min = np.min(ct[:, 0]), np.min(ct[:, 1])
        x_max, y_max = np.max(ct[:, 0]), np.max(ct[:, 1])
        height, width = image.shape
        x_center = (x_min + x_max) / (2 * width)
        y_center = (y_min + y_max) / (2 * height)
        yolo_w = (x_max - x_min) / width
        yolo_h = (y_max - y_min) / height
        x_center_list.append(x_center)
        y_center_list.append(y_center)
        yolo_w_list.append(yolo_w)
        yolo_h_list.append(yolo_h)
    return x_center_list, y_center_list, yolo_w_list, yolo_h_list


if __name__ == '__main__':
    #parameters
    filename = 'image.png'

    #load mask
    mask = cv2.imread(filename=filename, flags=0)

    #get x y w h
    x_center_list, y_center_list, yolo_w_list, yolo_h_list = get_x_y_w_h(
        image=mask)

    #print
    print(x_center_list, y_center_list, yolo_w_list, yolo_h_list)