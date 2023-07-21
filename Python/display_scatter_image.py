#import
import matplotlib.pyplot as plt
import cv2
from matplotlib.offsetbox import AnnotationBbox, OffsetImage

if __name__ == '__main__':
    #parameters
    filepath = 'dog.jpeg'
    x, y = 0, 0
    offset = 1

    #plot scatter
    fig, ax = plt.subplots(figsize=(16, 9), tight_layout=True)
    ax.scatter(x, y)
    img = cv2.imread(filepath)[..., ::-1]
    ab = AnnotationBbox(OffsetImage(img), (x + offset, y - offset))
    ax.add_artist(ab)
    ax.set_xticks(range(-5, 5))
    ax.set_yticks(range(-5, 5))
    fig.show()
