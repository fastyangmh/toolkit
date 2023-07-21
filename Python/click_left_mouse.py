#import
import cv2


#def
def click_left_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img=img,
                   center=(x, y),
                   radius=1,
                   color=(0, 0, 255),
                   thickness=-1)
        cv2.putText(img=img,
                    text=f'{x},{y}',
                    org=(x, y),
                    fontFace=cv2.FONT_HERSHEY_PLAIN,
                    fontScale=2,
                    color=(0, 0, 255),
                    thickness=2)
        cv2.imshow('image', img)


if __name__ == '__main__':
    #parameters
    filepath = 'image.png'

    #load image
    img = cv2.imread(filepath)

    #create window and monitor event
    cv2.namedWindow('image', cv2.WINDOW_KEEPRATIO)
    cv2.setMouseCallback('image', click_left_mouse)
    cv2.imshow('image', img)
    if cv2.waitKey(0) == 'q':
        cv2.destroyAllWindows()
