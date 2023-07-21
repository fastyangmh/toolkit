#import
import numpy as np


#def
def calculate_area(x1, y1, x2, y2):
    return (x2 - x1) * (y2 - y1)


def calculate_IOU(box1, box2):
    area1 = calculate_area(*box1)
    area2 = calculate_area(*box2)
    inter_w = min(box1[2], box2[2]) - max(box1[0], box2[0])
    inter_h = min(box1[3], box2[3]) - max(box1[1], box2[1])
    area_inter = inter_w * inter_h
    return area_inter / (area1 + area2 - area_inter)


if __name__ == '__main__':
    #parameters
    width = 1920
    height = 1080

    #generate boxes
    xx = sorted(np.random.randint(low=0, high=width, size=(2)))
    yy = sorted(np.random.randint(low=0, high=height, size=(2)))
    box1 = [xx[0], yy[0], xx[1], yy[1]]
    xx = sorted(np.random.randint(low=0, high=width, size=(2)))
    yy = sorted(np.random.randint(low=0, high=height, size=(2)))
    box2 = [xx[0], yy[0], xx[1], yy[1]]

    #calcuate iou
    print(calculate_IOU(box1=box1, box2=box2))
